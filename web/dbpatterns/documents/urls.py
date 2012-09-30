from django.conf.urls import include, patterns

from documents.resources import DocumentResource

urlpatterns = patterns('',

    (r'^api/', include(DocumentResource().urls)),

)