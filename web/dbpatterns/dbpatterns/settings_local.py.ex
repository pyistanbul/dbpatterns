import os

DEBUG = True

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
SECRET_KEY = 'g3a#n@4)q&9p7fx&uix9+abfi_#l_wr6uk&!plax$6)7*i(9vh'
