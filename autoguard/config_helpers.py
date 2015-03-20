from __future__ import unicode_literals

import urlparse
import warnings


def url_value_converter(value):
    value_to_convert = {
        'True': True,
        'False': False,
    }

    return value_to_convert.get(value, value)


def get_hostname(url):
    parsed = urlparse.urlparse(url)
    return parsed.hostname


def database_from_url(url):
    db_shortcuts = {
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
    parsed_qs = urlparse.parse_qs(parsed.query)
    config = {
        'backend': backend_shortcuts.get(parsed.scheme, parsed.scheme),
        'user': parsed.username,
        'password': parsed.password,
        'host': parsed.hostname,
        'port': parsed.port,
        'use_tls': False,
        'sender': "no-reply@{}".format(parsed.hostname if parsed.hostname else 'localhost'),
        'prefix': parsed_qs.get('prefix', ['[AUTOGUARD]'])[0],
    }
    config.update({
        key: url_value_converter(value[0])
        for key, value in urlparse.parse_qs(parsed.query).items()
    })
    return config


def sentry_caches_from_url(url):
    parsed = urlparse.urlparse(url)
    backend = parsed.scheme

    backends = {
        'redis': {
            'sentry': 'sentry.cache.redis.RedisCache',
            'buffer': 'sentry.buffer.redis.RedisBuffer',
            'tsdb': 'sentry.tsdb.redis.RedisTSDB',
            'quota': 'sentry.quotas.redis.RedisQuota',
            'rate_limits': 'sentry.ratelimits.redis.RedisRateLimiter',

            'redis_options': {'hosts': {0: {'host': parsed.hostname, 'port': parsed.port}}},
            'django_caches': {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}},
        },
        'memcached': {
            'sentry': 'sentry.cache.django.DjangoCache',
            'buffer': 'sentry.buffer.base.Buffer',  # TODO: check alternative backends
            'tsdb': 'sentry.tsdb.dummy.DummyTSDB',
            'quota': 'sentry.quotas.Quota',
            'rate_limits': 'sentry.ratelimits.base.RateLimiter',

            'redis_options': {},
            'django_caches': {'default': {
                'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
                'LOCATION': [parsed.netloc],
            }},
        }
    }

    return backends[backend]
