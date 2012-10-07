from django.conf.urls import patterns, include, url
from django.contrib import admin


urlpatterns = patterns('',

    # registration
    url(r'^accounts/', include('auth.urls')),

    # documents
    url(r'^', include('documents.urls')),

    # admin
    url(r'^admin/', include(admin.site.urls)),

)
