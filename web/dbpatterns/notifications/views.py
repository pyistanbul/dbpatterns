import json

from itertools import imap
from pymongo import DESCENDING

from django.http import HttpResponse
from django.views.generic import ListView

from notifications.models import Notification


class NotificationListView(ListView):

    template_name = "notifications/list.html"
    ajax_template_name = "notifications/notifications.html"
    context_object_name = "notifications"

    def get_queryset(self):
        notifications = self.get_notifications()
        return imap(Notification, notifications)

    def get_notifications(self):

        notifications = Notification.objects.filter_by_user_id(
            self.request.user.id)

        if self.request.is_ajax():
            return notifications.limit(5).sort([
                ("is_read", DESCENDING),
                ("date_created", DESCENDING)])

        return notifications.sort([("date_created", DESCENDING)])

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.ajax_template_name]
        return [self.template_name]

    def put(self, request, **kwargs):
        Notification.objects.mark_as_read(user_id=request.user.pk)
        return HttpResponse(json.dumps({
            "success": True
        }))
