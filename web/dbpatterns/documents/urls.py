from django.conf.urls import patterns, url
from django.views.generic import RedirectView

from documents.views import (HomeView, DocumentDetailView, ExportDocumentView, DocumentForksView,
                             DocumentStarsView, NewDocumentView, MyDocumentsView, DocumentEditView,
                             ForkDocumentView, StarDocumentView, SearchDocumentView)

urlpatterns = patterns('',

    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^documents/$', MyDocumentsView.as_view(), name='my_documents'),
    url(r'^documents/search$', SearchDocumentView.as_view(), name='search_document'),
    url(r'^documents/new$', NewDocumentView.as_view(), name='new_document'),
    url(r'^documents/(?P<slug>[-\w]+)/$', DocumentDetailView.as_view(), name='show_document'),
    url(r'^documents/(?P<slug>[-\w]+)/forks$', DocumentForksView.as_view(), name='show_document_forks'),
    url(r'^documents/(?P<slug>[-\w]+)/stars', DocumentStarsView.as_view(), name='show_document_stars'),
    url(r'^documents/(?P<slug>[-\w]+)/export/(?P<exporter>[-\w]+)$', ExportDocumentView.as_view(), name='export_document'),
    url(r'^documents/(?P<slug>[-\w]+)/edit$', DocumentEditView.as_view(), name='edit_document'),
    url(r'^documents/(?P<slug>[-\w]+)/fork$', ForkDocumentView.as_view(), name='fork_document'),
    url(r'^documents/(?P<slug>[-\w]+)/star$', StarDocumentView.as_view(), name='star_document'),


    # Legacy URLs
    url(r'^my-documents/$', RedirectView.as_view(url="/documents/")),
    url(r'^search/$', RedirectView.as_view(url="/documents/search")),
    url(r'^new/$', RedirectView.as_view(url="/documents/new")),
    url(r'^show/(?P<slug>[-\w]+)/$', RedirectView.as_view(url="/documents/%(slug)s/")),
    url(r'^show/(?P<slug>[-\w]+)/forks$', RedirectView.as_view(url="/documents/%(slug)s/forks")),
    url(r'^show/(?P<slug>[-\w]+)/stars', RedirectView.as_view(url="/documents/%(slug)s/stars")),
    url(r'^edit/(?P<slug>[-\w]+)/', RedirectView.as_view(url="/documents/%(slug)s/edit")),
    url(r'^export/(?P<slug>[-\w]+)/(?P<exporter>[-\w]+)', RedirectView.as_view(url="/documents/%(slug)s/export/%(exporter)s")),
    url(r'^fork/(?P<slug>[-\w]+)/$', RedirectView.as_view(url="/documents/%(slug)s/fork")),
    url(r'^star/(?P<slug>[-\w]+)/$', RedirectView.as_view(url="/documents/%(slug)s/star")),

)