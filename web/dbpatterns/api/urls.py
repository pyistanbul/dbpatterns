from django.conf.urls import url, include

from documents.resources import DocumentResource
from comments.resources import CommentResource
from profiles.resources import UserResource

urlpatterns = [
    url(r'^', include(DocumentResource().urls)),
    url(r'^', include(CommentResource().urls)),

    # django views
    url(r'^users/$', UserResource.as_view()),
]
