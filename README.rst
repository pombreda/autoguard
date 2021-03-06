autoguard
=========

The ``autoguard`` project is mostly a configuration setup for sentry.

It provides a standardized, easily configurable setup for that project.


Usage
-----

The ``autoguard`` configuration can be tuned in a few ways:

* Specific environment variables (starting with ``AUTOGUARD_``)
* Reading from ``/etc/autoguard/settings.ini``
* On a dev checkout, reading from ``/path/to/autoguard_checkout/local_settings.ini``

All options are described in ``example_settings.ini`` file.

Security
--------

Autoguard expects to run behind a **HTTPS** reverse proxy; that proxy *MUST* set the ``X-Forwarded-Proto`` HTTP header to ``https`` for HTTPS requests.


Setup
-----

Run the following commands:

.. code-block:: sh

    $ autoguard upgrade
    $ autoguard createsuperuser
    $ autoguard repair --owner=<superuser>
    $ autoguard start

The `autoguard` command is equivalent to `sentry --config=./autoguard/sentry_conf.py`.
