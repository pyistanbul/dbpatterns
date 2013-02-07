from lettuce import *

pages = {
    "create pattern page": "/documents/new",
    "my patterns": "/documents/",
    "newsfeed": "/",
}

@step("go to the (.*)")
def go_to_url(step, page):
    world.page_url = pages.get(page)
    world.page = world.browser.get(world.page_url)
    assert world.page.status_code == 200,\
    "Got %s" % world.page.status_code

@step('the redirected page should contains "(.*)"')
def should_redirected_page_contains(step, text):
    world.page = world.browser.get(world.page.get('Location'))
    assert text in world.page.content

@step('the page should contains "(.*)"')
def page_should_contains(step, text):
    assert text in world.page.content

@step('the page should not contains "(.*)"')
def page_should_not_contains(step, text):
    assert not text in world.page.content

@step('the page should return with (\d+) status code')
def should_return_with(step, status_code):
    assert world.page.status_code == int(status_code), status_code