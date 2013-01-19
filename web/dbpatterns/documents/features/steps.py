from lxml import html

from django.core.urlresolvers import reverse
from django.test import Client

from lettuce import *

from documents.models import Document

pages = {
    "create pattern page": "/documents/new",
    "my patterns": "/documents/",
}

@before.all
def set_browser():
    world.browser = Client()

@step('create a pattern that named "(.*)"')
@step('there is a pattern that named "(.*)"')
def create_pattern(step, title):
    world.created_document_id = Document.objects.collection.insert({
        "title": title,
        "user_id": world.user.id
    })

@step("go to the (.*)")
def go_to_url(step, page):
    world.page_url = pages.get(page)
    world.page = world.browser.get(world.page_url)
    assert world.page.status_code == 200, \
                "Got %s" % world.page.status_code

@step("go to the that pattern")
def go_to_created_pattern(step):
    document = Document.objects.get(_id=world.created_document_id)
    world.page = world.browser.get(document.get_absolute_url())
    assert world.page.status_code == 200,\
                "Got %s" % world.page.status_code

@step("look the stargazers of that pattern")
def go_to_created_pattern(step):
    url = reverse("show_document_stars",
        args=[str(world.created_document_id)])
    world.page = world.browser.get(url)

@step('type the title as "(.*)"')
def type_the_title(step, title):
    world.data = { "title": title }

@step('click to save button')
def click_to_save_button(step):
    world.page = world.browser.post(world.page_url, world.data)

@step('click to show button')
def click_to_show_button(step):
    dom = html.fromstring(world.page.content)
    show_link = dom.cssselect(".show")
    assert len(show_link) > 0
    world.page = world.browser.get(show_link[0].get("href"))

@step('click to star button')
def click_to_star_button(step):
    star_url = reverse("star_document", args=[str(world.created_document_id)])
    world.page = world.browser.post(star_url)

@step('click to fork button')
def click_to_fork_button(step):
    fork_url = reverse("fork_document", args=[str(world.created_document_id)])
    world.page = world.browser.get(fork_url, follow=False)

@step('the redirected page should contains "(.*)"')
def should_redirected_page_contains(step, text):
    world.page = world.browser.get(world.page.get('Location'))
    assert text in world.page.content, world.page.content

@step('the page should contains "(.*)"')
def page_should_contains(step, text):
    assert text in world.page.content, world.page.content

@step('the page should not contains "(.*)"')
def page_should_not_contains(step, text):
    assert not text in world.page.content

@step('the page should contains a form with "(.*)" field')
def page_should_contains_form(step, field):
    dom = html.fromstring(world.page.content)
    assert len(dom.cssselect("form")) > 0
    assert len(dom.cssselect("input[name='%s']" % field)) > 0

@step('Click the first delete button')
def click_the_first_delete_button(step):
    dom = html.fromstring(world.page.content)
    delete_links = dom.cssselect(".delete")
    assert len(delete_links) > 0
    assert world.browser.delete(delete_links[0].get("href")).status_code == 204

@step('fork the that pattern as "(.*)"')
def fork_the_created_pattern(step, title):
    fork_url = reverse("fork_document", args=[str(world.created_document_id)])
    world.page = world.browser.post(fork_url, {"title": title})

@step('go to the profile of "(.*)"')
def fork_the_created_pattern(step, username):
    world.page = world.browser.get(reverse("auth_profile", args=[username]))
    assert world.page.status_code == 200, "Got %s" % world.page.status_code

@step('I star that pattern')
def star_pattern(step):
    step.behave_as("""
    When go to the that pattern
    And click to star button
    """)