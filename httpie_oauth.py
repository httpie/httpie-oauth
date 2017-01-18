"""
OAuth 1.0a 2-legged plugin for HTTPie.

Supports HMAC-SHA1 and RSA-SHA1 signature methods.

If the authentication parameter is "username:password" then HMAC-SHA1 is used.
If the password is omitted (i.e. --auth username is provided), the user is
prompted for the password.

If the authentication parameter is "username::filename" (double colon between
the username and the filename) then RSA-SHA1 is used, and the PEM formatted
private key is read from that file. If the filename is omitted
(i.e. --auth username:: is provided), the user is prompted for
the filename. The username is used as the oauth_client_key OAuth parameter.

"""
import sys
from httpie.plugins import AuthPlugin
from requests_oauthlib import OAuth1
from oauthlib.oauth1 import SIGNATURE_RSA

__version__ = '2.0.0'
__author__ = 'Jakub Roztocil'
__licence__ = 'BSD'


class OAuth1Plugin(AuthPlugin):

    name = 'OAuth 1.0a 2-legged'
    auth_type = 'oauth1'
    description =\
        '--auth user:HMAC-SHA1_secret or --auth user::RSA-SHA1_privateKeyFile'

    def get_auth(self, username=None, password=None):
        if not password.startswith(':'):
            # HMAC-SHA1 signature method (--auth username:password)
            return OAuth1(client_key=username, client_secret=password)

        else:
            # RSA-SHA1 signature method (--auth username::filename)
            filename = password[1:]
            if len(filename) == 0:
                # Prompt for filename of RSA private key
                try:
                    filename = raw_input('http: filename of RSA private key: ')
                except EOFError:  # if ^D entered
                    sys.exit(1)

            try:
                key = open(filename).read()

                # Crude checks for correct file contents

                if key.find('-----BEGIN RSA PRIVATE KEY-----') == -1:
                    if key.find('-----BEGIN PUBLIC KEY-----') == -1:
                        err = 'does not contain a PEM formatted private key'
                    else:
                        err = 'wrong key, please provide the PRIVATE key'
                elif key.find('-----END RSA PRIVATE KEY-----') == -1:
                    err = 'private key is incomplete'
                else:
                    err = None
                if err is not None:
                    sys.stderr.write("http: " + filename + ': ' + err)
                    sys.exit(1)

                return OAuth1(client_key=username,
                              signature_method=SIGNATURE_RSA,
                              rsa_key=key)

            except IOError as e:
                sys.stderr.write("http: " + str(e))
                sys.exit(1)
