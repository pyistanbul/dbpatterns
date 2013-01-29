from django.test import Client

from lettuce import before, world

# load all steps
from .auth_steps import *
from .document_steps import *
from .form_steps import *
from .page_steps import *

@before.all
def set_browser():
    """
    Loads django's test client.
    """
    world.browser = Client()