from lxml import html
from lettuce import step, world

@step('type the "(.*)" as "(.*)"')
def type_the_field(step, field, value):
    world.data = {
        field: value
    }

@step('click to save button')
def click_to_save_button(step):
    world.page = world.browser.post(world.page_url, world.data)
    world.saved_url = world.page

@step('the page should contains a form with "(.*)" field')
def page_should_contains_form(step, field):
    dom = html.fromstring(world.page.content)
    assert len(dom.cssselect("form")) > 0
    assert len(dom.cssselect("input[name='%s']" % field)) > 0