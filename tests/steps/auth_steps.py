from lettuce import *

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

@step('I am logged in as user "(.*)"')
def login(step, username):
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password="123456")
    world.user = User.objects.get(username=username)
    assert world.browser.login(username=username, password="123456")

@step('I am logged out')
def logout(step):
    world.browser.logout()


@step('go to the profile of "(.*)"')
def fork_the_created_pattern(step, username):
    world.page = world.browser.get(reverse("auth_profile", args=[username]))
    assert world.page.status_code == 200, "Got %s" % world.page.status_code
