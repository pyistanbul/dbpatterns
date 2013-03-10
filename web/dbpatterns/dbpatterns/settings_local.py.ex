import os

DEBUG = True
TEMPLATE_DEBUG = True

COMPRESS_ENABLED = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), '../data'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}


GITHUB_APP_ID = "<<< GITHUB APP ID >>>"
GITHUB_API_SECRET = "<<< GITHUB SECRET KEY >>"

# Make this unique, and don't share it with anybody.
SECRET_KEY = '<<< SECRET KEY >>>'
