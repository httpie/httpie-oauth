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
        """
        Generate OAuth 1.0a 2-legged authentication for HTTPie.

        Note: Passpharse protected private keys are not yet supported.
        Before support can be implemented, the PyJWT, oauthlib and
        requests_oauthlib modules need to be updated.
        The passphrase needs to be obtained here and passed
        through to PyJWT's jwt/algorithms.py, line 168, where currently it
        passes into load_pem_private_key a hardcoded value of None for the
        password.
        To get it to there, many places in oauthlib's oauth1/rfc5849/__init__.py
        and oauth1/rfc5849/signature.py, as well as in requests_oauthlib's
        oauth1_auth.py, need to be updated to pass it through.

        :param username: username
        :param password: password, or colon followed by a filename
        :return: requests_oauthlib.oauth1_auth.OAuth1 object
        """
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

            key = OAuth1Plugin.read_private_key(filename)

            return OAuth1(client_key=username,
                          signature_method=SIGNATURE_RSA,
                          rsa_key=key)

    @staticmethod
    def read_private_key(filename):
        """
        Check if the key is a recognised private key format.

        Prints an error message to stderr and exits if it is not. Uses
        crude checks to try and generate more useful error messages.

        :param filename: file to read private key from
        :return: PEM formatted private key
        """
        try:
            key = open(filename).read()

            if key.find('-----BEGIN RSA PRIVATE KEY-----') == -1:
                # Did not find the start of private key.

                if key.find('-----BEGIN PUBLIC KEY-----') != -1 or \
                   key.find('-----BEGIN RSA PUBLIC KEY-----') != -1 or \
                   key.find('ssh-rsa ') != -1 or \
                   key.find('---- BEGIN SSH2 PUBLIC KEY ----') != -1:
                    # Appears to contain a PKCS8, PEM, OpenSSH old or
                    # OpenSSH new format public key.
                    # The newer OpenSSH format does not follow RFC7468
                    # and only has 4 hyphens and spaces around the text!
                    err = 'wrong key, please provide the PRIVATE key'
                elif key.find('-----BEGIN OPENSSH PRIVATE KEY-----') != -1:
                    # Appears to contain newer OpenSSH private key format
                    err = 'private key format not supported' + \
                          ', PEM format required'
                else:
                    # Generic error message
                    err = 'does not contain a PEM formatted private key'

            elif key.find('-----END RSA PRIVATE KEY-----') == -1:
                # Found start of private key, but not its end
                err = 'private key is incomplete'
            else:
                err = None
            if err is not None:
                sys.stderr.write("http: " + filename + ': ' + err)
                sys.exit(1)

            return key

        except IOError as e:
            sys.stderr.write("http: " + str(e))
            sys.exit(1)
