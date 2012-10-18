### dbpatterns.com

Dbpatterns is a service that allows you to create, share, explore database models on the web.

### Installation

Install mongodb:

    sudo apt-get install mongodb
    # or on mac
    sudo brew install mongodb

Start mongodb:

    mongod

Create a virtual env:

    virtualenv dbpatterns
    source dbpatterns/bin/activate

Clone the repository and install requirements:

    cd dbpatterns
    git clone git://github.com/fatiherikli/dbpatterns.git
    pip install -r dbpatterns/conf/requirements.pip

Create a file that named settings_local.py
Configure the database and secret key.

    cd dbpatterns/web/dbpatterns
    vim settings_local.py

The example of configuration:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'data',
            'USER': '',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
        }
    }

    SECRET_KEY = '<SECRET-KEY>'

And run the following commands:

    cd ../
    python manage.py syncdb
    python manage.py runserver

That's all. You can access to dbpatterns from http://127.0.0.1:8000