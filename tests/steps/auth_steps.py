from lxml import html
from lettuce import *

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from profiles.models import FollowedProfile

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
def go_to_profile(step, username):
    world.page = world.browser.get(reverse("auth_profile", args=[username]))
    assert world.page.status_code == 200, "Got %s" % world.page.status_code

@step('go to my profile')
def go_to_my_profile(step):
    step.given('go to the profile of "%s"' % world.user)

@step('should I follow "(.*)"')
def should_have_follow(step, username):
    assert world.user.following.filter(following__username=username).exists()

@step('following users exist')
def following_users_exist(step):
    for user_hash in step.hashes:
        user = user_hash.copy()
        password = user.pop("password", None)
        user, created = User.objects.get_or_create(**user)
        user.set_password(password)
        user.save()

@step('click to follow button')
def click_to_follow_button(step):
    dom = html.fromstring(world.page.content)
    follow_link = dom.cssselect(".follow")
    assert len(follow_link) > 0
    world.page = world.browser.post(follow_link[0].get("href"))

@step('click to unfollow button')
def click_to_unfollow_button(step):
    dom = html.fromstring(world.page.content)
    unfollow_link = dom.cssselect(".unfollow")
    assert len(unfollow_link) > 0
    world.page = world.browser.delete(unfollow_link[0].get("href"))

@step('"(.*)" following "(.*)"')
def follow(step, from_username, to_username):
    follower = User.objects.get(username=from_username)
    following = User.objects.get(username=to_username)
    FollowedProfile.objects.create(follower=follower, following=following)