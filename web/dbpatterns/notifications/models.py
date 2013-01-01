from datetime import datetime
from bson import ObjectId

from django.core.urlresolvers import reverse
from django.dispatch import receiver

from comments.signals import comment_done
from documents import get_collection
from documents.models import Document
from documents.signals import fork_done, star_done
from notifications.constants import NOTIFICATION_TYPE_COMMENT, NOTIFICATION_TYPE_FORK, NOTIFICATION_TYPE_STAR, NOTIFICATION_TYPE_FOLLOWING, NOTIFICATION_TEMPLATES
from profiles.management.signals import follow_done

class NotificationManager(object):

    def create(self, ):
        pass

class Notification(dict):
    """
    A model that wraps mongodb document
    """
    objects = NotificationManager()

    def get_absolute_url(self):
        url_resolvers = {
            NOTIFICATION_TYPE_COMMENT:
                lambda: reverse("show_document",
                    args=[self.get("object_id")]),

            NOTIFICATION_TYPE_FORK:
                lambda: reverse("show_document",
                    args=[self.get("object_id")]),

            NOTIFICATION_TYPE_STAR:
                lambda: reverse("show_document",
                    args=[self.get("object_id")]),

            NOTIFICATION_TYPE_FOLLOWING:
                lambda: reverse("auth_profile",
                    args=[self.get("sender").get("username")]),

        }
        return url_resolvers[self.get("type")]()


    def as_text(self):
        return NOTIFICATION_TEMPLATES[self.get("type")] % self.get("sender")


@receiver(comment_done)
def create_comment_notification(instance, **kwargs):
    newsfeed = get_collection("notifications")
    newsfeed.insert({
        "is_read": False,
        "object_id": instance.document._id,
        "type": NOTIFICATION_TYPE_COMMENT,
        "date_created": datetime.today(),
        "sender": {
            "username": instance.user.username,
            "email": instance.user.email # it's required for gravatar
        },
        "recipient": instance.document.user_id
    })

@receiver(fork_done)
def create_fork_notification(instance, **kwargs):
    newsfeed = get_collection("notifications")
    forked_document = Document.objects.get(
            _id=ObjectId(instance.fork_of))
    newsfeed.insert({
        "is_read": False,
        "object_id": instance._id,
        "type": NOTIFICATION_TYPE_FORK,
        "date_created": instance.date_created,
        "sender": {
            "username": instance.user.username,
            "email": instance.user.email # it's required for gravatar
        },
        "recipient": forked_document.user_id
    })


@receiver(star_done)
def create_star_notification(instance, user, **kwargs):
    newsfeed = get_collection("notifications")
    newsfeed.insert({
        "is_read": False,
        "object_id": instance._id,
        "type": NOTIFICATION_TYPE_STAR,
        "date_created": instance.date_created,
        "sender": {
            "username": user.username,
            "email": user.email # it's required for gravatar
        },
        "recipient": instance.user_id
    })

@receiver(follow_done)
def create_following_notification(following, follower, **kwargs):
    newsfeed = get_collection("notifications")
    newsfeed.insert({
        "is_read": False,
        "object_id": follower.id,
        "type": NOTIFICATION_TYPE_FOLLOWING,
        "date_created": datetime.now(),
        "sender": {
            "username": follower.username,
            "email": follower.email # it's required for gravatar
        },
        "recipient": following.id
    })