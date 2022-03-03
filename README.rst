
ℹ️ Please use the newer `httpie-oauth1` plugin instead:

https://github.com/qcif/httpie-oauth1

------


httpie-oauth
===========

OAuth plugin for `HTTPie <https://httpie.org/>`_.

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


You can also use `HTTPie sessions <https://httpie.org/doc#sessions>`_:

.. code-block:: bash

    # Create session
    $ http --session=logged-in --auth-type=oauth1 --auth='client-key:client-secret' example.org

    # Re-use auth
    $ http --session=logged-in POST example.org hello=world

