from restfly.endpoint import APIEndpoint

class AssessmentAPI(APIEndpoint):
    def create_type(self, subscription, guid, **properties):
        '''
        Create a new assessment type for the subscription defined.

        Args:
            subscription (str): The subscription id.
            guid (str): The new assessment GUID to create.
            **properties (dict):
                Properties to associate to the new assessment type.
        '''
        return self._api.put(
            'subscriptions/{}/providers/Microsoft.Security/assessmentMetadata/{}'.format(
                subscription, guid),
            params={'api-version': '2019-01-01-preview'},
            json={
                'tags': {'provider': 'Tenable'},
                'properties': properties
            }).json()

    def create_assessment_finding(self, resource, type_guid, status, **data):
        '''
        Create/updates an assessment finding on the defined resource & type.

        Args:
            resource (str): The resource id.
            type_guid (str): The assessment type GUID.
            status (str):
                The health status of the finding.  The API supports the values:
                ``Healthy``, ``Unhealthy``, and ``NotApplicable``.
            **data (dict):
                Additional datapoints to be added into the ``additionalData``
                sub-document.
        '''
        return self._api.put(
            '{}/providers/Microsoft.Security/assessments/{}'.format(
                resource[1:], type_guid),
            params={'api-version': '2019-01-01-preview'},
            json={
                'properties': {
                    'resourceDetails': {
                        'Source': 'Azure',
                        'Id': resource,
                    },
                    'status': {'code': status},
                    'additionalData': data,
                }
            }).json()
