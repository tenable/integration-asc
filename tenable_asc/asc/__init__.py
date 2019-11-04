import adal
from tenable_asc import __version__
from restfly.session import APISession
from .assessments import AssessmentAPI

class AzureSecurityCenter(APISession):
    _vendor='Tenable',
    _product='Azure Security Center',
    _build=__version__
    _url = 'https://management.azure.com'
    _auth_url = 'https://login.microsoftonline.com'

    def __init__(self, tenant_id, app_id, app_secret, **kw):
        self._auth_url = kw.pop('auth_url', self._auth_url)
        self._tenant_id = tenant_id
        self._app_id = app_id
        self._app_secret = app_secret
        super(AzureSecurityCenter, self).__init__(**kw)

    def _build_session(self, **kwargs):
        super(AzureSecurityCenter, self)._build_session(**kwargs)

        # Retreive the access token using the adal library.
        self._ctx = adal.AuthenticationContext('{}/{}'.format(
            self._auth_url, self._tenant_id))
        resp = self._ctx.acquire_token_with_client_credentials(self._url + '/',
            self._app_id, self._app_secret)

        # add the auth bearer header to the session.
        self._session.headers.update({
            'Authorization': 'Bearer {}'.format(resp.get('accessToken'))
        })

    @property
    def assessments(self):
        return AssessmentAPI(self)