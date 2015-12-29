import os
from os.path import join

from configurations import Configuration, values

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Base(Configuration):
    # Absolute path to the directory static files should be collected to.
    # Don't put anything in this directory yourself; store your static files
    # in apps' "static/" subdirectories and in STATICFILES_DIRS.
    # Example: "/home/media/media.lawrence.com/static/"
    STATIC_ROOT = join(BASE_DIR, 'static')

    # URL prefix for static files.
    # Example: "http://media.lawrence.com/static/"
    STATIC_URL = '/assets/'

    # Additional locations of static files
    STATICFILES_DIRS = (
        join(BASE_DIR, 'assets'),
    )

    TEMPLATE_DIRS = (
        join(BASE_DIR, 'templates'),
    )

    DATABASES = values.DatabaseURLValue(alias='default', environ_name='DATABASE_URL')

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = values.SecretValue()

    ########## DEBUG
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
    DEBUG = values.BooleanValue(True)

    LOG_ROOT = join(BASE_DIR, 'log')


    ########## RESTFRAMEWORK

    REST_FRAMEWORK = {
        'PAGINATE_BY': 10,
        'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
    }

    ########## BOOTSTRAP 3
    BOOTSTRAP3 = {
        'jquery_url': '//code.jquery.com/jquery.min.js',
        'base_url': '//netdna.bootstrapcdn.com/bootstrap/3.1.1/',
        'css_url': None,
        'theme_url': None,
        'javascript_url': None,
        'horizontal_label_class': 'col-md-2',
        'horizontal_field_class': 'col-md-4',
    }


    ########## CELERY
    BROKER_URL = 'amqp://'
    CELERY_RESULT_BACKEND = 'amqp://'
    CELERY_TASK_RESULT_EXPIRES=3600

    from datetime import timedelta
    from celery.schedules import crontab

    CELERYBEAT_SCHEDULE = {
        # Executes onecontrol sync_devices every 30 minutes
        'onecontrol_sync_devices': {
        'task': 'apps.core.tasks.onecontrol_sync_devices',
        'schedule': timedelta(seconds=1800),
        },
         # Executes every night at 3:00 A.M
        'onecontrol_get_port_volume': {
        'task': 'apps.core.tasks.onecontrol_get_port_volume',
        'schedule': crontab(hour=3, minute=0),
        },
        # Executes every night at 4:00 A.M
        'onecontrol_get_service_volume': {
        'task': 'apps.core.tasks.onecontrol_get_service_volume',
        'schedule': crontab(hour=4, minute=0),
        },
        # Executes every night at 2:00 A.M
        'surf_syncdb': {
        'task': 'apps.core.tasks.surf_syncdb',
        'schedule': crontab(hour=2, minute=0),
        },
        # Executes every night at 5:00 A.M
        'bubbles_create_parents_services': {
        'task': 'apps.core.tasks.bubbles_create_parent_services',
        'schedule': crontab(hour=5, minute=0),
        },
        # Executes every night at 6:00 A.M
        'surf_utils_fix_missing_datapoints': {
        'task': 'apps.core.tasks.surf_utils_fix_missing_datapoints',
        'schedule': crontab(hour=6, minute=0),
        },
    }

    # Where to chdir at start.
    CELERYBEAT_CHDIR=BASE_DIR

    # Extra arguments to celerybeat
    CELERYBEAT_OPTS="--schedule={}/run/celerybeat-schedule".format(BASE_DIR)


    ######### BOWER
    BOWER_COMPONENTS_ROOT = join(BASE_DIR, 'static')

    BOWER_INSTALLED_APPS = (
        'd3#3.3.6',
        'nvd3#1.1.12-beta',
    )

    ######### HAYSTACK

    HAYSTACK_CONNECTIONS = {
        'default': {
            #'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
            'ENGINE': 'bubbles.elastic.ConfigurableElasticSearchEngine',
            'URL': 'http://127.0.0.1:9200/',
            'INDEX_NAME': 'haystack',
                    },
      }

    ELASTICSEARCH_DEFAULT_ANALYZER = "snowball"

    ELASTICSEARCH_INDEX_SETTINGS = {
        'settings': {
            "analysis": {
                "analyzer": {
                    "ngram_analyzer": {
                        "type": "custom",
                        "tokenizer": "lowercase",
                        "filter": ["haystack_ngram"]
                    },
                    "edgengram_analyzer": {
                        "type": "custom",
                        "tokenizer": "whitespace",
                        "filter": ["haystack_edgengram"]
                    }
                },
                "tokenizer": {
                    "haystack_ngram_tokenizer": {
                        "type": "nGram",
                        "min_gram": 3,
                        "max_gram": 15,
                    },
                    "haystack_edgengram_tokenizer": {
                        "type": "edgeNGram",
                        "min_gram": 2,
                        "max_gram": 15,
                        "side": "front"
                    }
                },
                "filter": {
                    "haystack_ngram": {
                        "type": "nGram",
                        "min_gram": 3,
                        "max_gram": 15
                    },
                    "haystack_edgengram": {
                        "type": "edgeNGram",
                        "min_gram": 4,
                        "max_gram": 15
                    }
                }
            }
        }
    }


class Dev(Base):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    )

    MANAGERS = ADMINS

    # Make this unique, and don't share it with anybody.
    SECRET_KEY = values.SecretValue()

    ########## INSTALLED_APPS
    INSTALLED_APPS = Base.INSTALLED_APPS
    ########## END INSTALLED_APPS

    ########## Mail settings
    EMAIL_HOST = "localhost"
    EMAIL_PORT = 1025
    EMAIL_BACKEND = values.Value('django.core.mail.backends.console.EmailBackend')
    ########## End mail settings

    ########## django-debug-toolbar
    MIDDLEWARE_CLASSES = Base.MIDDLEWARE_CLASSES + ('debug_toolbar.middleware.DebugToolbarMiddleware',)
    INSTALLED_APPS += ('debug_toolbar',
                       'django_extensions',)

    INTERNAL_IPS = ('127.0.0.1',)

    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
        'SHOW_TEMPLATE_CONTEXT': True,
    }
    ########## end django-debug-toolbar


class Prod(Base):
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG

    ADMINS = (
    # ('Your Name', 'your_email@example.com'),
    )

    MANAGERS = ADMINS

    ALLOWED_HOSTS = values.ListValue(['example.com'])

    ########## INSTALLED_APPS
    INSTALLED_APPS = Base.INSTALLED_APPS
    ########## END INSTALLED_APPS

    INSTALLED_APPS += ('gunicorn',)

    # A sample logging configuration. The only tangible logging
    # performed by this configuration is to send an email to
    # the site admins on every HTTP 500 error when DEBUG=False.
    # See http://docs.djangoproject.com/en/dev/topics/logging for
    # more details on how to customize your logging configuration.
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
            },
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
        },
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            }
        },
        'handlers': {
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'logfile': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': "{}/{}".format(Base.LOG_ROOT, 'bubbles.log'),
                'maxBytes': 50000000,
                'backupCount': 2,
                'formatter': 'verbose',
            },
        },
        'loggers': {
            'django.request': {
                'handlers': ['mail_admins'],
                'level': 'ERROR',
                'propagate': True,
            },
            'apps.core': {
                'handlers': ['console', 'logfile'],
                'level': 'DEBUG',
            },
        }
    }
