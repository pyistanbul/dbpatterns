import logging
import os
import sys

from django.conf import settings
from django.core.management import call_command
from django.test.simple import DjangoTestSuiteRunner

from lettuce import *

from documents.models import Document
from newsfeed.models import Entry
from notifications.models import Notification


@before.all
def switch_to_test_database():
    """
    Switching to the test database
    """
    logging.info("Setting up a test database ...\n")

    try:
        from south.management.commands import patch_for_test_db_setup

        patch_for_test_db_setup()
    except ImportError:
        pass

    world.test_runner = DjangoTestSuiteRunner(interactive=False)
    world.test_runner.setup_test_environment()
    world.test_db = world.test_runner.setup_databases()
    call_command('syncdb', **{
        'settings': settings.SETTINGS_MODULE,
        'interactive': False,
        'verbosity': 0})

    # Reload mongodb database
    settings.MONGODB_DATABASE = settings.MONGODB_TEST_DATABASE
    for model in [Document, Entry, Notification]:
        model.objects.load()
        model.objects.collection.remove()


@after.all
def after_all(total):
    logging.info("Destroy test database ...\n")

    # Destroy database.
    world.test_runner.teardown_databases(world.test_db)

    # Tear Down the test environment.
    world.test_runner.teardown_test_environment()


@after.each_scenario
def before_each_feature(scenario):
    logging.info("Flusing db ... \n")

    call_command('flush', **{
        'settings': settings.SETTINGS_MODULE,
        'interactive': False})


def setup_test_directory():
    sys.path.append(os.path.join(os.path.dirname(__file__), "../../tests"))
    __import__("steps")


setup_test_directory()