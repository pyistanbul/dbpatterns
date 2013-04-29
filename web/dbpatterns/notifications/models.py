from datetime import datetime
from bson import ObjectId

from django.core.urlresolvers import reverse
from django.dispatch import receiver
from pymongo import DESCENDING

from comments.signals import comment_done
from documents import get_collection
from documents.models import Document
from documents.signals import fork_done, star_done, assignment_done
from profiles.management.signals import follow_done
from notifications.constants import (NOTIFICATION_TYPE_COMMENT,
                                     NOTIFICATION_TYPE_FORK,
                                     NOTIFICATION_TYPE_STAR,
                                     NOTIFICATION_TYPE_FOLLOWING,
                                     NOTIFICATION_TEMPLATES,
                                     NOTIFICATION_TYPE_ASSIGNMENT)


class NotificationManager(object):
    """
    A class that allows create, edit, read notifications.
    """

    def __init__(self):
        self.load()

    def load(self):
        self.collection = get_collection("notifications")
        self.collection.ensure_index([
            ("date_created", DESCENDING),
        ])

    def filter_by_user_id(self, user_id):
        """
        Shows the notifications of user.
        """
        return self.collection.find({
            "recipient": user_id,
        })

    def mark_as_read(self, user_id):
        """
        Marks as read the notifications of user.
        """
        self.collection.update(
            {"recipient": user_id, "is_read": False},
            {"$set": {"is_read": True}}, multi=True)

    def create(self, object_id, notification_type, sender, recipient_id):
        """
        Creates notification from provided parameters.
        """
        # if the sender affect the own document,
        # ignore it.
        if not sender.id == recipient_id:
            self.collection.insert({
                "is_read": False,
                "object_id": object_id,
                "type": notification_type,
                "date_created": datetime.today(),
                "sender": {
                    "username": sender.username,
                    "email": sender.email  # it's required for gravatar
                },
                "recipient": recipient_id
            })


class Notification(dict):
    """
    A model that wraps mongodb document
    """
    objects = NotificationManager()

    def get_absolute_url(self):
        url_resolvers = {
            NOTIFICATION_TYPE_COMMENT:
                lambda: reverse("show_document", args=[self.get("object_id")]),

            NOTIFICATION_TYPE_FORK:
                lambda: reverse("show_document", args=[self.get("object_id")]),

            NOTIFICATION_TYPE_STAR:
                lambda: reverse("show_document", args=[self.get("object_id")]),

            NOTIFICATION_TYPE_ASSIGNMENT:
                lambda: reverse("edit_document", args=[self.get("object_id")]),

            NOTIFICATION_TYPE_FOLLOWING:
                lambda: reverse("auth_profile",
                                args=[self.get("sender").get("username")]),

        }
        return url_resolvers[self.get("type")]()

    def as_text(self):
        return NOTIFICATION_TEMPLATES[self.get("type")] % self.get("sender")


@receiver(comment_done)
def create_comment_notification(instance, **kwargs):
    """
    Sends notification to the user of commented document.
    """
    Notification.objects.create(
        object_id=instance.document._id,
        notification_type=NOTIFICATION_TYPE_COMMENT,
        sender=instance.user,
        recipient_id=instance.document.user_id
    )


@receiver(fork_done)
def create_fork_notification(instance, **kwargs):
    """
    Sends notification to the user of forked document.
    """
    forked_document = Document.objects.get(
        _id=ObjectId(instance.fork_of))

    Notification.objects.create(
        object_id=instance._id,
        notification_type=NOTIFICATION_TYPE_FORK,
        sender=instance.user,
        recipient_id=forked_document.user_id
    )


@receiver(star_done)
def create_star_notification(instance, user, **kwargs):
    """
    Sends notification to the user of starred document.
    """
    Notification.objects.create(
        object_id=instance._id,
        notification_type=NOTIFICATION_TYPE_STAR,
        sender=user,
        recipient_id=instance.user_id
    )


@receiver(follow_done)
def create_following_notification(following, follower, **kwargs):
    """
    Sends notification to the followed user from the follower.
    """
    Notification.objects.create(
        object_id=follower.id,
        notification_type=NOTIFICATION_TYPE_FOLLOWING,
        sender=follower,
        recipient_id=following.id
    )


@receiver(assignment_done)
def create_assignment_notification(instance, user_id, **kwargs):
    """
    Sends notification to the assigned users on the document
    """
    Notification.objects.create(
        object_id=instance.id,
        notification_type=NOTIFICATION_TYPE_ASSIGNMENT,
        sender=instance.user,
        recipient_id=user_id
    )
