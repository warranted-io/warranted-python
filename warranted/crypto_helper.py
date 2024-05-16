import hmac
import hashlib
from functools import reduce
from operator import xor

def time_safe_compare(a, b):
    """
    Function does a timesafe comparison
    @param {string} a - the first string
    @param {string} b - the second string
    @returns {boolean} - true if they're equal, else false.
    """
    a_bytes = a.encode("utf-8")
    b_bytes = b.encode("utf-8")
    if len(a_bytes) != len(b_bytes):
        return False
    result = reduce(xor, [(a_bytes[i] ^ b_bytes[i]) for i in range(len(a_bytes))], 0)
    return result == 0

def create_hmac(url, json_data, secret_key, algorithm="sha256"):
    """
    Function to create HMAC of a JSON request
    @param {string} url - the destination url
    @param {string} json_data - JSON request data
    @param {string} secret_key - Secret key for HMAC
    @param {string} algorithm - Hashing algorithm (e.g., 'sha256', 'sha512')
    @returns {string} - HMAC value
    """
    algo = getattr(hashlib, algorithm)
    hmac_obj = hmac.new(secret_key.encode("utf-8"), digestmod=algo)
    hmac_obj.update((url + json_data).encode("utf-8"))
    return hmac_obj.hexdigest()