import os
from .base import *

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        
    }
}
'''

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_URL = '/static/'


STATICFILES_DIRS = [BASE_DIR.child('static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')





