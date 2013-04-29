from django.conf.urls import patterns, url

from documents.views import (DocumentDetailView, ExportDocumentView,
                             DocumentForksView, DocumentStarsView,
                             NewDocumentView, MyDocumentsView, DocumentEditView,
                             ForkDocumentView, StarDocumentView,
                             SearchDocumentView)

urlpatterns = patterns(
    '',
    url(r'^$', MyDocumentsView.as_view(), name='my_documents'),
    url(r'^search$', SearchDocumentView.as_view(), name='search_document'),
    url(r'^new$', NewDocumentView.as_view(), name='new_document'),
    url(r'^(?P<slug>[-\w]+)/$', DocumentDetailView.as_view(),
        name='show_document'),
    url(r'^(?P<slug>[-\w]+)/forks$', DocumentForksView.as_view(),
        name='show_document_forks'),
    url(r'^(?P<slug>[-\w]+)/stars', DocumentStarsView.as_view(),
        name='show_document_stars'),
    url(r'^(?P<slug>[-\w]+)/export/(?P<exporter>[-\w]+)$',
        ExportDocumentView.as_view(), name='export_document'),
    url(r'^(?P<slug>[-\w]+)/edit$', DocumentEditView.as_view(),
        name='edit_document'),
    url(r'^(?P<slug>[-\w]+)/fork$', ForkDocumentView.as_view(),
        name='fork_document'),
    url(r'^(?P<slug>[-\w]+)/star$', StarDocumentView.as_view(),
        name='star_document'),

)