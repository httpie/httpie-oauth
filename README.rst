httpie-oauth
===========

OAuth plugin for `HTTPie <https://github.com/jkbr/httpie>`_.

It currently provides support for OAuth 1.0a 2-legged.


Installation
------------

.. code-block:: bash

    $ pip install httpie-oauth


You should now see ``oauth1`` under ``--auth-type`` in ``$ http --help`` output.


Usage
-----

.. code-block:: bash

    $ http --auth-type=oauth1 --auth='client-key:client-secret' example.org


You can also use `HTTPie sessions <https://github.com/jkbr/httpie#sessions>`_:

.. code-block:: bash

    # Create session
    $ http --session=logged-in --auth-type=oauth1 --auth='client-key:client-secret' example.org

    # Re-use auth
    $ http --session=logged-in POST example.org hello=world

