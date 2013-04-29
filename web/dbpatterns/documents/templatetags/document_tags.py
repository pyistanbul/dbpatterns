from django import template
from documents.resources import DocumentResource

register = template.Library()


@register.simple_tag()
def document_count_for_user(user):
    resource = DocumentResource()
    return resource.get_collection().find({
        "user_id": user.pk
    }).count()