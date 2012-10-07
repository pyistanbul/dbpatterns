from django.conf.urls import patterns, include, url


urlpatterns = patterns('',

    # registration
    url(r'^accounts/', include('auth.urls')),

    # documents
    url(r'^', include('documents.urls')),

)
