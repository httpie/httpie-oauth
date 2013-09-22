"""
OAuth plugin for HTTPie.

"""
from httpie.plugins import AuthPlugin
from requests_oauthlib import OAuth1


__version__ = '1.0.0'
__author__ = 'Jakub Roztocil'
__licence__ = 'BSD'


class OAuth1Plugin(AuthPlugin):

    name = 'OAuth 1.0a 2-legged'
    auth_type = 'oauth1'
    description = ''

    def get_auth(self, username, password):
        return OAuth1(client_key=username, client_secret=password)
