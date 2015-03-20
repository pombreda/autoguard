from __future__ import unicode_literals

import urlparse
import warnings


def url_value_converter(value):
    value_to_convert = {
        'True': True,
        'False': False,
    }

    return value_to_convert.get(value, value)


def database_from_url(url):
    db_shortcuts = {
        'postgresql': 'django.db.backends.postgresql_psycopg2',
        'postgres': 'django.db.backends.postgresql_psycopg2',
        'sqlite': 'django.db.backends.sqlite3',
    }

    parsed = urlparse.urlparse(url)
    parsed_qs = urlparse.parse_qs(parsed.query)
    if any([len(value) > 1 for value in parsed_qs.values()]):
        warnings.warn("settings: django.db_url: one argument is set more than once, only use first one.")

    return {
        'ENGINE': db_shortcuts.get(parsed.scheme, parsed.scheme),
        'NAME': parsed.path[1:],
        'USER': parsed.username,
        'PASSWORD': parsed.password,
        'HOST': parsed.hostname,
        'PORT': parsed.port,
        'OPTIONS': {
            key: url_value_converter(value[0])
            for key, value in parsed_qs.items()
        }
    }


def mail_from_url(url):
    backend_shortcuts = {
        'smtp': 'django.core.mail.backends.smtp.EmailBackend',
        'console': 'django.core.mail.backends.console.EmailBackend',
    }

    parsed = urlparse.urlparse(url)
    config = {
        'backend': backend_shortcuts.get(parsed.scheme, parsed.scheme),
        'user': parsed.username,
        'password': parsed.password,
        'host': parsed.hostname,
        'port': parsed.port,
        'use_tls': False,
        'sender': "no-reply@{}".format(parsed.hostname if parsed.hostname else 'localhost')
    }
    config.update({
        key: url_value_converter(value[0])
        for key, value in urlparse.parse_qs(parsed.query).items()
    })
    return config


def cache_from_url(url):
    backend_shortcuts = {
        'db': 'django.core.cache.backends.db.DatabaseCache',
        'dummy': 'django.core.cache.backends.dummy.DummyCache',
        'file': 'django.core.cache.backends.filebased.FileBasedCache',
        'mem': 'django.core.cache.backends.locmem.LocMemCache',
        'memcached': 'django.core.cache.backends.memcached.MemcachedCache'
    }

    parsed = urlparse.urlparse(url)
    return {
        'BACKEND': backend_shortcuts.get(parsed.scheme, parsed.scheme),
        'LOCATION': parsed.netloc,
    }


def sentry_buffer_from_url(url):
    backend_shortcuts = {
        'base': 'sentry.buffer.base.Buffer',
        'redis': 'sentry.buffer.redis.RedisBuffer',
    }

    parsed = urlparse.urlparse(url)
    config = {
        'backend': backend_shortcuts.get(parsed.scheme, parsed.scheme),
        'options': {},
    }

    if config['backend'] == backend_shortcuts['redis']:
        config['options'] = {
            'hosts': {
                0: {
                    'host': parsed.hostname,
                    'port': parsed.port,
                }
            }
        }

    return config
