import json

from lxml import html
from lettuce import *

from django.core.urlresolvers import reverse

from documents.models import Document
from documents.signals import document_done

@step('create a pattern that named "(.*)"')
@step('there is a pattern that named "(.*)"')
def create_pattern(step, title):
    world.created_document_id = Document.objects.collection.insert({
        "title": title,
        "user_id": world.user.id
    })
    created_document = Document.objects.get(_id=world.created_document_id)
    document_done.send(instance=created_document, sender=step)

@step("go to the created pattern")
def go_to_created_pattern(step):
    document_id = Document.objects.collection.find_one().get("_id")
    world.page = world.browser.get(reverse("show_document", args=[document_id]))

@step("go to the that pattern")
def go_to_pattern(step):
    document = Document.objects.get(_id=world.created_document_id)
    world.page = world.browser.get(document.get_absolute_url())
    assert world.page.status_code == 200, \
                    "Got %s" % world.page.status_code

@step("look the stargazers of that pattern")
def go_to_created_pattern(step):
    url = reverse("show_document_stars",
        args=[str(world.created_document_id)])
    world.page = world.browser.get(url)

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

@step('submit the comment')
def submit_comment(step):
    comments_resource_uri = reverse("api_get_comments",
        args=["documents", str(world.created_document_id)])
    data = world.data.copy()
    data["username"] = world.user.username
    world.page = world.browser.post(comments_resource_uri, json.dumps(data),
        content_type="application/json")
    assert world.page.status_code == 201, "Got %s" % world.page.status_code

@step('the comments of that pattern')
def comments_of_pattern(step):
    comments_resource_uri = reverse("api_get_comments",
        args=["documents", str(world.created_document_id)])
    world.page = world.browser.get(comments_resource_uri)
    assert world.page.status_code == 200, "Got %s" % world.page.status_code

@step("the comment count of that pattern should be (\d+)")
def comment_count_of_pattern(step, comment_count):
    document = Document.objects.get(_id=world.created_document_id)
    assert document.comment_count == int(comment_count)

@step('choose the "(.*)" option as "(.*)"')
def choose_radio_button(step, name, value):
    world.data[name] = value

@step('I star that pattern')
def star_pattern(step):
    step.behave_as("""
    When go to the that pattern
    And click to star button
    """)

@step('I leave a comment on that pattern')
def star_pattern(step):
    step.behave_as("""
    When go to the that pattern
    And I type the "body" as "Test Comment"
    When I submit the comment
    """)