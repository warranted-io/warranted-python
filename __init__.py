import os
import platform
import requests
import sys
from urllib.parse import urlencode

from crypto_helper import create_hmac, time_safe_compare
from warranted_exception import WarrantedException

version = '1.0.0'

class Client:
    def __init__(self, account_id, auth_token):
        """
        Warranted Client Constructor
        @param {string} account_id - the account id
        @param {string} auth_token - the primary auth token
        """
        if not account_id:
            raise WarrantedException('No account_id provided')
        if not auth_token:
            raise WarrantedException('No auth_token provided')
        self.account_id = account_id
        self.auth_token = auth_token
        self.host = 'https://app.warranted.io'
        self.headers = {}

    def set_host(self, host):
        """
        Set an alternate host. This can be helpful for compatability with proxies.
        @param {string} host - an alternate host, the prefix of all API requests
        """
        self.host = host

    def set_headers(self, headers):
        """
        Set additional headers. This can be helpful for compatability with proxies.
        @param {object} headers - headers to add with any API requests
        """
        self.headers.update(headers)

    def _get_user_agent_header(self):
        """
        Internal method to get the user agent header
        @returns {string} - the user agent header
        """
        os_name = platform.system()
        architecture = platform.architecture()[0]
        python_version = sys.version.split(' ')[0]

        return f"warranted-python/{version} ({os_name} {architecture}) Python/{python_version}"

    def _get_request_headers(self):
        """
        Internal method to get request headers
        @returns {object} - the headers for a request
        """
        return {
            'User-Agent': self._get_user_agent_header(),
            **self.headers
        }

    class _Decisions:
        def __init__(self, client):
            """
            Decisions Constructor
            @param {object} client - the warranted client
            """
            self.client = client

        def get(self, decision_id):
            """
            Get details about a decision
            @param {string} decisionId - the id of the decision to fetch
            @returns {object} - Details at: http://app.warranted.io/docs/decisions
            """
            url = f'{self.client.host}/api/v1/decisions/{decision_id}'
            response = requests.get(url, auth=(self.client.account_id, self.client.auth_token), headers=self.client._get_request_headers())
            return response.json()

    decisions = _Decisions

    class _LawEnforcementRequests:
        def __init__(self, client):
            """
            LawEnforcementRequests Constructor
            @param {object} client - the warranted client
            """
            self.client = client

        def get(self, options):
            """
            Get either a list of lawEnforcementRequests or one specific request
            @param {object | string} options - Optional. If an object, it should contain either a `startAt` or `limit` parameter or both.
            If a string it should be a `lawEnforcementRequestId`.
            @returns {array | object} - Details at: http://app.warranted.io/docs/lawEnforcementRequests
            """
            url = f'{self.client.host}/api/v1/lawEnforcementRequests'
            if isinstance(options, str):
                url += f'/{options}'
            elif isinstance(options, dict):
                params = {}
                if 'startAt' in options:
                    params['startAt'] = int(options['startAt'])
                if 'limit' in options:
                    params['limit'] = int(options['limit'])
                url += '?' + urlencode(params)
            
            response = requests.get(url, auth=(self.account_id, self.auth_token), headers=self.client._get_request_headers())
            return response.json()

        def add(self, law_enforcement_request_file):
            """
            Submit a new lawEnforcementRequest
            @param {file} lawEnforcementRequestFile - a law enforcement request file pointer. Only pdfs are accepted.
            @returns {object} - Details at: http://app.warranted.io/docs/lawEnforcementRequests
            """
            file_name = os.path.basename(law_enforcement_request_file.name)
            form_data = {'lawEncforementRequest': (file_name, law_enforcement_request_file)}
            url = f'{self.host}/api/v1/lawEnforcementRequest/new'
            response = requests.post(url, auth=(self.account_id, self.auth_token), headers=self.client._get_request_headers(), files=form_data)
            return response.json()

        def update(self, law_enforcement_request_id, data):
            """
            Update a lawEnforcementRequest
            @param {object} lawEnforcementRequest - an updated law enforcement request object.
            @returns {object} - Details at: http://app.warranted.io/docs/lawEnforcementRequests
            """
            url = f'{self.client.host}/api/v1/lawEnforcementRequests/{law_enforcement_request_id}'
            response = requests.put(url, json=data, auth=(self.client.account_id, self.client.auth_token), headers=dict({'Content-Type': 'application/json'}, **self.client._get_request_headers()))
            return response.json()

        def delete(self, law_enforcement_request_id):
            """
            elete a lawEnforcementRequest
            @param {string} lawEnforcementRequestId - a law enforcement request id.
            @returns {object} - Details at: http://app.warranted.io/docs/lawEnforcementRequests
            """
            url = f'{self.client.host}/api/v1/lawEnforcementRequests/{law_enforcement_request_id}'
            response = requests.delete(url, auth=(self.client.account_id, self.client.auth_token), headers=self.client._get_request_headers())
            return response.json()

    law_enforcement_requests = _LawEnforcementRequests

    class _Me:
        def __init__(self, client):
            """
            Me Constructor
            @param {object} client - the warranted client
            """
            self.client = client

        def get(self):
            """
            Get data about the current user
            @returns {object} - Details at: http://app.warranted.io/docs/me
            """
            url = f'{self.client.host}/api/v1/me'
            response = requests.get(url, auth=(self.client.account_id, self.client.auth_token), headers=self.client._get_request_headers())
            return response.json()

    me = _Me

    class _Schema:
        def __init__(self, client):
            """
            Schema Constructor
            @param {object} client - the warranted client
            """
            self.client = client

        def get(self):
            """
            Get the schema
            @returns {object} - Details at: http://app.warranted.io/docs/schema
            """
            url = f'{self.client.host}/api/v1/schema'
            response = requests.get(url, auth=(self.client.account_id, self.client.auth_token), headers=self.client._get_request_headers())
            return response.json()

        def update(self, schema):
            """
            Update the schema
            @param {object} schema - the updated schema
            @returns {object} - Details at: http://app.warranted.io/docs/schema
            """
            url = f'{self.client.host}/api/v1/schema'
            response = requests.put(url, json=schema, auth=(self.client.account_id, self.client.auth_token), headers=dict({'Content-Type': 'application/json'}, **self.client._get_request_headers()))
            return response.json()

    schema = _Schema

    def validate_request(self, signature, url, body):
        """
        Validate the signature of a request
        @param {string} signature - the signature from the X-Warranted-Signature to compare against
        @param {string} url - the url that received the request
        @param {string} body - JSON request data
        @returns {boolean} - whether or not the signature matches
        """
        hmac = create_hmac(url, body, self.auth_token)
        return time_safe_compare(signature, hmac)