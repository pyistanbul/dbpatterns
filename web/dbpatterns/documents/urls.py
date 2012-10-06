from django.conf.urls import include, patterns, url

from documents.resources import DocumentResource
from documents.views import HomeView, DocumentView

urlpatterns = patterns('',

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^show/(?P<slug>[-\w]+)/$', DocumentView.as_view(), name='show_document'),
    url(r'^edit/(?P<slug>[-\w]+)/$', DocumentView.as_view(), name='edit_document'),

    # api
    url(r'^api/', include(DocumentResource().urls)),

)