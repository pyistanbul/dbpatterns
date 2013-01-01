from itertools import imap
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import ListView
from pymongo import DESCENDING

from notifications.models import Notification
from documents import get_collection


class NotificationListView(ListView):

    template_name = "notifications/list.html"
    ajax_template_name = "notifications/notifications.html"
    context_object_name = "notifications"

    def get_queryset(self):

        get_collection("notifications").ensure_index([
            ("date_created", DESCENDING),
        ])

        notifications = self.get_notifications()
        return imap(Notification, notifications)

    def get_notifications(self):

        notifications = get_collection("notifications").find({
            "recipient": self.request.user.id,
        })

        if self.request.is_ajax():

            return notifications.limit(5).sort([
                ("is_read", DESCENDING),
                ("date_created", DESCENDING)
            ])

        return notifications.sort([
            ("date_created", DESCENDING)
        ])

    def get_template_names(self):
        if self.request.is_ajax():
            return [self.ajax_template_name]
        return [self.template_name]

    def put(self, request, **kwargs):
        get_collection("notifications").update(
            { "recipient": request.user.id,
              "is_read": False },
            { "$set": {
                "is_read": True }}
        )
        return HttpResponse(json.dumps({
            "success": True
        }))
