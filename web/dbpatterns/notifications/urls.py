from django.conf.urls import url

from notifications.views import NotificationListView


urlpatterns = [
    url(r'^$', NotificationListView.as_view(),
        name='notifications'),
]
