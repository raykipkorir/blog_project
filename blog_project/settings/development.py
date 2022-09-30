from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

#database 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'