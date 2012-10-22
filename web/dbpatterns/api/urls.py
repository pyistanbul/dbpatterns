from django.conf.urls import patterns, url, include

from documents.resources import DocumentResource
from comments.resources import CommentResource

urlpatterns = patterns('',

    url(r'^', include(DocumentResource().urls)),
    url(r'^', include(CommentResource().urls)),

)