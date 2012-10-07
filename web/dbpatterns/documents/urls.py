from django.conf.urls import include, patterns, url

from documents.resources import DocumentResource
from documents.views import HomeView, DocumentDetailView, NewDocumentView, MyDocumentsView, DocumentEditView, ForkDocumentView, StarDocumentView

urlpatterns = patterns('',

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^my-documents/$$', MyDocumentsView.as_view(), name='my_documents'),
    url(r'^new/$$', NewDocumentView.as_view(), name='new_document'),
    url(r'^show/(?P<slug>[-\w]+)/$', DocumentDetailView.as_view(), name='show_document'),
    url(r'^edit/(?P<slug>[-\w]+)/$', DocumentEditView.as_view(), name='edit_document'),
    url(r'^fork/(?P<slug>[-\w]+)/$', ForkDocumentView.as_view(), name='fork_document'),
    url(r'^star/(?P<slug>[-\w]+)/$', StarDocumentView.as_view(), name='star_document'),

    # api
    url(r'^api/', include(DocumentResource().urls)),

)