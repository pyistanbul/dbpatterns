from django.test import Client
from django.contrib.auth.models import User

from lettuce import *

from documents.models import Document

pages = {
    "create pattern page": "/documents/new",
    "my patterns": "/documents/",
}

@before.all
def set_browser():
    world.browser = Client()

@step('I am logged in as user "(.*)"')
def login(step, username):
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(username=username, password="123456")

    world.user = User.objects.get(username=username)

    assert world.browser.login(username=username, password="123456")

@step('create a pattern that named "(.*)"')
def create_pattern(step, title):
    Document.objects.collection.insert({
        "title": title,
        "user_id": world.user.id
    })

@step("go to the (.*)")
def go_to_url(step, page):
    world.page_url = pages.get(page)
    world.page = world.browser.get(world.page_url)
    assert world.page.status_code == 200, \
                "Got %s" % world.page.status_code

@step('I type the title as "(.*)"')
def type_the_title(step, title):
    world.data = { "title": title }

@step('I click to save button')
def click_to_save_button(step):
    world.page = world.browser.post(world.page_url, world.data)

@step('the page should redirect to (.*)')
def should_redirect_to_edit_page(step, url):
    assert world.page.status_code, 301

@step('the redirected page should contains "(.*)"')
def should_redirected_page_contains(step, text):
    world.page = world.browser.get(world.page.get('Location'))
    assert text in world.page.content

@step('the page should contains "(.*)"')
def should_page_contains(step, text):
    assert text in world.page.content

