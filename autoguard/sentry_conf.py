# -*- coding: utf-8 -*-
# Copyright (c) 2014-2015 Polyconseil SAS.
# This code is distributed under the two-clause BSD License.

from __future__ import unicode_literals
import base64
import logging
import os
import os.path
import urlparse

from getconf import ConfigGetter

from .config_helpers import database_from_url, cache_from_url, mail_from_url, sentry_buffer_from_url

PROJECT_NAME = 'autoguard'  # Name of the project (e.g GitHub repository)
CONFIG = ConfigGetter(
    PROJECT_NAME,
    '/etc/%s/settings.ini' % PROJECT_NAME,
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'local_settings.ini')),
)

# Django Configuration
# ====================
DEBUG = CONFIG.getbool('dev.debug', False, doc="Enable debug mode.")
TIME_ZONE = CONFIG.get('django.time_zone', default='Europe/Paris')
SECRET_KEY = CONFIG.get('django.secret_key', base64.b64encode(os.urandom(40)))

DATABASES = {
    'default': database_from_url(CONFIG.get('django.db_uri', 'sqlite:///sentry.sqlite'))
}

CACHES = {
    'default': cache_from_url(CONFIG.get('django.cache_uri', 'mem://'))
}

_parsed_email_url = mail_from_url(CONFIG.get('django.mail_uri', 'console://?sender=no-reply@localhost'))
EMAIL_BACKEND = _parsed_email_url['backend']
EMAIL_HOST = _parsed_email_url['host']
EMAIL_PORT = _parsed_email_url['port']
EMAIL_USER = _parsed_email_url['user']
EMAIL_PASSWORD = _parsed_email_url['password']
EMAIL_USE_TLS = _parsed_email_url['use_tls']
SERVER_EMAIL = _parsed_email_url['sender']

BROKER_URL = CONFIG.get('django.queue_broker_url', default=None)
CELERY_ALWAYS_EAGER = BROKER_URL is None

_site_parsed_url = urlparse.urlparse(CONFIG.get('django.site_url', 'http://localhost:9000'))
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", _site_parsed_url.hostname]
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True

# Sentry Configuration
# ====================
SENTRY_URL_PREFIX = _site_parsed_url.geturl()

SENTRY_WEB_HOST = CONFIG.get('host', '127.0.0.1')
SENTRY_WEB_PORT = CONFIG.getint('port', 9000)
SENTRY_WEB_OPTIONS = {
    'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},
    'workers': CONFIG.getint('sentry.workers', 5),
}

_parsed_sentry_buffer = sentry_buffer_from_url(CONFIG.get('sentry.buffer_uri', 'base://'))
SENTRY_BUFFER = _parsed_sentry_buffer['backend']
SENTRY_BUFFER_OPTIONS = _parsed_sentry_buffer['options']

SENTRY_PUBLIC = CONFIG.getbool('sentry.public', default=False, doc="Whether not authenticated user can read data.")
SENTRY_SAMPLE_DATA = CONFIG.getbool('sentry.sample_data', default=True, doc="Use data sampling.")

SENTRY_ALLOW_REGISTRATION = False  # no auto-registration
SOCIAL_AUTH_CREATE_USERS = False  # no auto-registration

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
