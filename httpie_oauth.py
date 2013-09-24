"""
OAuth plugin for HTTPie.

"""
from httpie.plugins import AuthPlugin


__version__ = '1.0.2'
__author__ = 'Jakub Roztocil'
__licence__ = 'BSD'


class OAuth1Plugin(AuthPlugin):

    name = 'OAuth 1.0a 2-legged'
    auth_type = 'oauth1'
    description = ''

    def get_auth(self, username, password):
        from requests_oauthlib import OAuth1
        return OAuth1(client_key=username, client_secret=password)
