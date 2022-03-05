
ℹ️ Please use the newer `httpie-oauth1` plugin instead:

https://github.com/qcif/httpie-oauth1

------


httpie-oauth
============

OAuth 1.0a two-legged plugin for `HTTPie <https://httpie.org/>`_.


Installation
------------

.. code-block:: bash

    $ pip install httpie-oauth


You should now see ``oauth1`` under ``--auth-type`` in the
``$ http --help`` output.

To be able to use the RSA-SHA1 signature type, also install **PyJWT**
and PyCA's **cryptography** package.

.. code-block:: bash

    $ pip install pyjwt
    $ pip install cryptography

On CentOS 7, it might be easier to use *yum* to install "epel-release"
and then the "python2-cryptography" packages, since to *pip install* it
requires C code to be compiled.

Usage
-----

HMAC-SHA1
.........

To use the HMAC-SHA1 signature method, in the ``--auth`` parameter
provide the client-key, a single colon and the client-secret.

.. code-block:: bash

    $ http --auth-type=oauth1 --auth='client-key:client-secret' example.org

It will interactively prompt for the client-secret, if there is no colon.
If the password starts with a colon, use this interactive method to enter it
(otherwise the extra colon will cause it to use RSA-SHA1 instead of HMAC-SHA1).

RSA-SHA1
........

To use the RSA-SHA1 signature method, in the ``--auth`` parameter
provide the client key, two colons and the name of a file containing
the RSA private key. The file must contain a PEM formatted RSA private
key.

.. code-block:: bash

    $ http --auth-type=oauth1 --auth='client-key::filename' example.org

It will interactively prompt for the filename, if there is no value
after the two colons.

The filename can also be a relative or absolute path to the file.

Passphrase protected private keys are not supported.

Including the client key in the private key file
++++++++++++++++++++++++++++++++++++++++++++++++

If the client key in the ``--auth`` parameter is empty (i.e. the
option argument is just two colons and the filename), the
``oauth_consumer_key`` parameter from the file is used.  It must
appear in the file before the private key.

For example, if the private key file contains something like this:

::

    oauth_consumer_key: myconsumerkey
    -----BEGIN RSA PRIVATE KEY-----
    ...
    -----END RSA PRIVATE KEY-----

It can be used with this command:

.. code-block:: bash

    $ http --auth-type=oauth1 --auth=::filename example.org


HTTPie Sessions
...............

You can also use `HTTPie sessions <https://httpie.org/doc#sessions>`_:

.. code-block:: bash

    # Create session
    $ http --session=logged-in --auth-type=oauth1 --auth='client-key:client-secret' example.org

    # Re-use auth
    $ http --session=logged-in POST example.org hello=world


Troubleshooting
...............

ImportError: No module named jwt.algorithms
+++++++++++++++++++++++++++++++++++++++++++

The *PyJWT* module is not available. Please install it.

AttributeError: 'module' object has no attribute 'RSAAlgorithm'
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

The PyCA's *cryptography* module is not available. Please install it.
