from .base import *

DEBUG = False

SLACK_API_TOKEN = 'notsotoken'
SLACK_DEBUG = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
    },
    'loggers': {
        'slack': {
            'handlers': ['null'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
