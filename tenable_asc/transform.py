import arrow, time, logging, json
from restfly.errors import NotFoundError, ForbiddenError

class Tio2ASC:
    _cache = dict()
    _psubs = list()
    allowed_subs = None

    def __init__(self, tio, asc):
        self._log = logging.getLogger('{}.{}'.format(
            self.__module__, self.__class__.__name__))
        self.tio = tio
        self.asc = asc

    def _cache_asset(self, asset):
        '''
        Populate the asset counter sub-doc into the cache dictionary.
        '''
        resource = asset.get('azure_resource_id')
        if resource:
            self._cache[asset['id']] = {
                'resource': resource,
                'subscription': resource.split('/')[2],
                'low': 0,
                'medium': 0,
                'high': 0,
                'critical': 0,
            }
            self._log.debug(
                'Found Tenable Asset {} with Azure Resource ID of {}'.format(
                    asset['id'], resource))

    def _upsert_metadata(self, asset_uuid, unhealthy_thresh):
        '''
        upserts the data for the asset UUID from the cache into ASC.

        Args:
            asset_uuid (str): The Tenable.io UUID to process.
            unhealthy_thresh (str):
                At what severity level will a non-zero counter flip the status
                to "unhealthy"?
        '''

        # a simple severity matrix to track what each threshold means.
        matrix = {
            'low': ['low', 'medium', 'high', 'critical'],
            'medium': ['medium', 'high', 'critical'],
            'high': ['high', 'critical'],
            'critical': ['critical',],
        }

        atype = 'ae3222be-cd0a-4ca2-b85e-2ecaf3392b18'
        asset = self._cache[asset_uuid]

        # Lets determine the status of the asset.
        status = 'Healthy'
        for sev in matrix[unhealthy_thresh]:
            if asset[sev] > 0:
                status = 'Unhealthy'

        # The resource must be in an allowed subscription if the allowed
        # subscription list is defined.
        if (not self.allowed_subs
          or (self.allowed_subs and asset['subscription'] in self.allowed_subs)):
            # If the subscription hasn't yet received the assessment type, then
            # we will need to create it.
            if not asset['subscription'] in self._psubs:
                resp = self.asc.assessments.create_type(asset['subscription'], atype,
                    displayName='Tenable.io Assessment',
                    assessmentType='Custom',
                    description='Vulnerabilities were discovered on the resource.',
                    remediationDescription='Refer to details within Tenable.io for more information',
                    categories=['Compute',],
                    secureScoreWeight=50,
                    preview=True,
                )
                self._psubs.append(asset['subscription'])
                self._log.debug('Azure Responded with: ' + json.dumps(resp))

            # Generate the finding in Azure Security Center.
            try:
                resp = self.asc.assessments.create_assessment_finding(
                    asset['resource'],
                    atype,
                    status,
                    low=asset['low'],
                    medium=asset['medium'],
                    high=asset['high'],
                    critical=asset['critical'],
                    link=''.join([
                        'https://cloud.tenable.com/tio/app.html#',
                        '/vulnerability-management/assets/asset-details',
                        '/{}/overview'.format(asset_uuid)
                    ]))
            except NotFoundError:
                self._log.warning('Asset no longer exists {}'.format(
                    asset['resource']))
            except ForbiddenError:
                self._log.warning('Not authorized to submit resource {}'.format(
                    asset['resource']))
            else:
                self._log.debug('Azure Responded with: ' + json.dumps(resp))

    def ingest(self, age=None, batch_size=1000, unhealthy_thresh='medium'):
        '''
        Perform the ingestion

        Args:
            age (int, optional):
                What is the maximum age of the assets and vulnerability
                observations?  If left unspecified, the default is the timestamp
                from 90 days ago.
            batch_size (int, optional):
                What is the chunk sizing to use when exporting the data from
                Tenable.io?  If left unspecified, the default is 1000.
            unhealthy_thresh (str, optional):
                At what point do we consider the asset in an unhealthy state?
                Based on a non-zero number of vulns of the specified severity
                level.
        '''
        if not age:
            age = arrow.utcnow().shift(days=-90).timestamp
        self._cache = dict()

        # First we need to populate the cache with the assets that we actually
        # care about.  To do this we will run an asset export and then pass each
        # asset on to the _cache_asset method, which simply checks to see if the
        # azure_resource_id attribute is populated, and if so, will generate the
        # base sub-dictionary with all of the counters and meta-data that we
        # need for later on.
        self._log.info('querying Tenable.io for the asset records.')
        assets = self.tio.exports.assets(sources=['AZURE'], updated_at=age)
        for asset in assets:
            self._cache_asset(asset)
        self._log.info('discovered {} Azure Assets'.format(len(self._cache)))

        # Now we will initiate the vulnerability export and then leverage the
        # cache that we had just generated to count up the number of vulns for
        # each severity level.
        self._log.info('querying Tenable.io for vulnerability records.')
        vulns = self.tio.exports.vulns(
            last_found=age,
            severity=['low', 'medium', 'high', 'critical'],
            state=['open', 'reopened'])

        # Iterate through the vulnerabilities, incrementing the appropriate
        # severity counter for eligable assets.
        vcounter = 0
        for vuln in vulns:
            if vuln['asset']['uuid'] in self._cache.keys():
                vcounter += 1
                self._cache[vuln['asset']['uuid']][vuln['severity']] += 1
        self._log.info('processed {} vulnerabilities out of {} total.'.format(
            vcounter, vulns.count))

        # Iterate over the cache and feed the data into ASC.
        for asset in self._cache.keys():
            self._upsert_metadata(asset, unhealthy_thresh)