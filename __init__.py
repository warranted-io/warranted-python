from crypto_helper import create_hmac, time_safe_compare
from warranted_exception import WarrantedException

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