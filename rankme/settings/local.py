from . import get_env_variable
from .base import *

DEBUG = bool(get_env_variable('DEBUG', True))
SECRET_KEY = 'notsosecret'
