from django.test import Client
from lettuce import before, step, world

from django.conf import settings

from documents.models import Document
from newsfeed.models import Entry
from notifications.models import Notification

# load all steps
from .auth_steps import *
from .document_steps import *
from .form_steps import *
from .page_steps import *


@before.all
def switch_to_test_database():
    """
    Switching to the test database
    """
    settings.MONGODB_DATABASE = settings.MONGODB_TEST_DATABASE

    # Reload mongodb connections
    for model in [Document, Entry, Notification]:
        model.objects.load()
        model.objects.collection.remove()

@before.all
def set_browser():
    """
    Loads django's test client.
    """
    world.browser = Client()