from django.conf.urls import patterns, url

from notifications.views import NotificationListView


urlpatterns = patterns('',

    url(r'^$', NotificationListView.as_view(), name='notifications'),

)