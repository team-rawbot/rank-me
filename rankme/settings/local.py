from . import get_env_variable
from .base import *

DEBUG = bool(get_env_variable('DEBUG', True))
TEMPLATE_DEBUG = DEBUG
SECRET_KEY = 'notsosecret'

SOCIAL_AUTH_TWITTER_KEY = get_env_variable('SOCIAL_AUTH_TWITTER_KEY', 'notsotwitter')
SOCIAL_AUTH_TWITTER_SECRET = get_env_variable('SOCIAL_AUTH_TWITTER_SECRET', 'notsotwitter')

INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

INTERNAL_IPS = ('127.0.0.1', '10.0.2.1')
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

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
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'slack': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    }
}

SLACK_DEBUG = True
