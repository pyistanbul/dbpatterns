from lettuce import before, world, step, after

from django.contrib.auth.models import User
from django.conf import settings

from documents.models import Document
from newsfeed.models import Entry
from notifications.models import Notification

# test environment configuration
def reload_mongodb_connections():
    """
    Reloads the collections of models.
    """
    for model in [Document, Entry, Notification]:
        model.objects.load()
        model.objects.collection.remove()

@before.all
def switch_to_test_database():
    """
    Switching to the test database
    """
    settings.MONGODB_DATABASE = settings.MONGODB_TEST_DATABASE
    reload_mongodb_connections()

# global steps
@step('I am logged in as user "(.*)"')
def login(step, username):
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password="123456")
    world.user = User.objects.get(username=username)
    assert world.browser.login(username=username, password="123456")
