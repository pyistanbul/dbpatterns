from django.conf.urls import url, patterns
from django.views.generic import RedirectView

urlpatterns = patterns(
    '',
   # Legacy URLs

    url(r'^my-documents/$',
        RedirectView.as_view(url="/documents/")),
    url(r'^search/$',
        RedirectView.as_view(url="/documents/search")),
    url(r'^new/$',
        RedirectView.as_view(url="/documents/new")),
    url(r'^show/(?P<slug>[-\w]+)/$',
        RedirectView.as_view(url="/documents/%(slug)s/")),
    url(r'^show/(?P<slug>[-\w]+)/forks$',
        RedirectView.as_view(
            url="/documents/%(slug)s/forks")),
    url(r'^show/(?P<slug>[-\w]+)/stars',
        RedirectView.as_view(
            url="/documents/%(slug)s/stars")),
    url(r'^edit/(?P<slug>[-\w]+)/', RedirectView.as_view(
        url="/documents/%(slug)s/edit")),
    url(r'^export/(?P<slug>[-\w]+)/(?P<exporter>[-\w]+)',
        RedirectView.as_view(
            url="/documents/%(slug)s/export/%(exporter)s")),
    url(r'^fork/(?P<slug>[-\w]+)/$', RedirectView.as_view(
        url="/documents/%(slug)s/fork")),
    url(r'^star/(?P<slug>[-\w]+)/$', RedirectView.as_view(
        url="/documents/%(slug)s/star")),
)