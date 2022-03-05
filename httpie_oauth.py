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
import string
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
            # HMAC-SHA1 signature method (--auth client-key:client-secret)
            return OAuth1(client_key=username, client_secret=password)

        else:
            # RSA-SHA1 signature method (--auth oauth_consumer_key::filename)
            filename = password[1:]
            if len(filename) == 0:
                # Prompt for filename of RSA private key
                try:
                    filename = raw_input('http: filename of RSA private key: ')
                except EOFError:  # if ^D entered
                    sys.exit(1)

            username, key = OAuth1Plugin.read_private_key(username, filename)

            return OAuth1(client_key=username,
                          signature_method=SIGNATURE_RSA,
                          rsa_key=key)

    @staticmethod
    def read_private_key(username, filename):
        """
        Check if the key is a recognised private key format.

        Prints an error message to stderr and exits if it is not. Uses
        crude checks to try and generate more useful error messages.

        :param username: username to use
        :param filename: file to read private key from
        :return: PEM formatted private key
        """
        PEM_PRIVATE_KEY_BEGINNING = '-----BEGIN RSA PRIVATE KEY-----'
        PEM_PRIVATE_KEY_ENDING = '-----END RSA PRIVATE KEY-----'
        ATTR_NAME = 'oauth_consumer_key'

        try:
            data = open(filename).read()

            key_start = data.find(PEM_PRIVATE_KEY_BEGINNING)
            key_end = data.find(PEM_PRIVATE_KEY_ENDING)

            if key_start == -1:
                # Did not find the start of private key.

                if data.find('-----BEGIN PUBLIC KEY-----') != -1 or \
                   data.find('-----BEGIN RSA PUBLIC KEY-----') != -1 or \
                   data.find('ssh-rsa ') != -1 or \
                   data.find('---- BEGIN SSH2 PUBLIC KEY ----') != -1:
                    # Appears to contain a PKCS8, PEM, OpenSSH old or
                    # OpenSSH new format public key.
                    # The newer OpenSSH format does not follow RFC7468
                    # and only has 4 hyphens and spaces around the text!
                    err = 'wrong key, please provide the PRIVATE key'
                elif data.find('-----BEGIN OPENSSH PRIVATE KEY-----') != -1:
                    # Appears to contain newer OpenSSH private key format
                    err = 'private key format not supported' + \
                          ', PEM format required'
                else:
                    # Generic error message
                    err = 'does not contain a PEM formatted private key'

            else:
                if key_end == -1:
                    err = 'private key is incomplete'
                else:
                    key_end += len(PEM_PRIVATE_KEY_ENDING)
                    err = None

            # If the username is blank, try to extract a username from the file

            if len(username) == 0 and err is None:
                username, err = OAuth1Plugin.extract_username(data, ATTR_NAME,
                                                              0, key_start)

            if err is not None:
                sys.stderr.write("http: " + filename + ': ' + err)
                sys.exit(1)

            pem_key = data[key_start:key_end]

            return username, pem_key

        except IOError as e:
            sys.stderr.write("http: " + str(e))
            sys.exit(1)

    @staticmethod
    def extract_username(data, attr_name, start, end, limit=8096):
        """
        Extract a named parameter from the contents.

        :param data: text to search
        :param attr_name: name of attribute to look for
        :param start: index into contents of where to start looking
        :param end: index into contents of where to stop looking
        :param limit: upper limit for end position
        :return: client-key value or None if not found
        """
        stop_pos = end
        if limit < end:
            stop_pos = limit
        i = start

        while i < stop_pos:
            eol_pos = data.find('\n', i, stop_pos)
            if eol_pos == -1:
                break  # no more complete lines found

            colon_pos = data.find(':', i, eol_pos)
            if colon_pos != -1:
                name = data[i:colon_pos].strip()
                value = data[colon_pos + 1: eol_pos].strip()
                if name == attr_name:
                    return value, None  # successfully found
            i = eol_pos + 1

        if limit < end:
            return None, '"{}" not found in first {} characters'.format(
                         attr_name, limit)
        else:
            return None, '"{}" not found before private key'.format(attr_name)
