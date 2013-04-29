from bson import ObjectId
from datetime import datetime

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from comments.models import Comment
from comments.signals import comment_done, comment_delete
from documents import get_collection
from documents.models import Document
from documents.signals import document_done, fork_done, star_done, document_delete, fork_delete
from profiles.management.signals import follow_done, unfollow_done
from newsfeed.constants import (NEWS_TYPE_COMMENT, NEWS_TYPE_DOCUMENT,
                                NEWS_TYPE_FORK, NEWS_TYPE_STAR,
                                NEWS_TYPE_FOLLOWING, NEWS_TYPE_REGISTRATION)

RELATED_MODELS = {
    NEWS_TYPE_COMMENT: Comment,
    NEWS_TYPE_DOCUMENT: Document,
    NEWS_TYPE_FORK: Document,
    NEWS_TYPE_STAR: Document
}


class EntryManager(object):
    """
    A manager that allows you to manage newsfeed items.
    """

    def __init__(self):
        self.load()

    def load(self):
        self.collection = get_collection("newsfeed")

    def create(self, object_id, news_type, sender, recipients=None,
               related_object=None):
        """
        Creates newsfeed item from provided parameters
        """

        followers = sender.followers.values_list("follower_id", flat=True)
        recipients = (recipients if recipients is not None
                      else list(followers) + [sender.pk])

        entry_bundle = {
            "object_id": object_id,
            "news_type": news_type,
            "date_created": datetime.now(),
            "sender": {
                "username": sender.username,
                "email": sender.email  # it's required for gravatar
            },
            "recipients": recipients
        }

        # sometimes we have to create custom related object bundle.
        # for example: following actions. because user actions are
        # holding on relational database.
        if related_object is not None:
            entry_bundle["related_object"] = related_object

        self.collection.insert(entry_bundle)

    def add_to_recipients(self, following, follower):
        """
        Adds the id of follower to the recipients of followed profile's entries.
        """
        self.collection.update(
            {"sender.username": following.username},
            {"$push": {"recipients": follower.id}}, multi=True)

    def remove_from_recipients(self, following, follower):
        """
        Removes follower id from the recipients of followed profile's entries.
        """
        self.collection.update(
            {"sender.username": following.username},
            {"$pull": {"recipients": follower.id}}, multi=True)

    def delete(self, object_type, object_id):
        """
        Removes news entry from provided object type and object id.
        """
        self.collection.remove({
            "news_type": object_type,
            "object_id": object_id})


class Entry(dict):
    """
    A model that wraps mongodb document for newsfeed.
    """
    objects = EntryManager()

    @property
    def related_object(self):
        news_type = self.get("news_type")
        object_id = self.get("object_id")
        model = RELATED_MODELS.get(news_type)

        if model is None:
            return self.get("related_object")

        return model.objects.get(_id=ObjectId(object_id))


@receiver(comment_done)
@receiver(fork_done)
@receiver(document_done)
def create_news_entry(instance, **kwargs):
    """
    Creates news entries for the following types:

        - Comments
        - Forks
        - Documents

    That models have `get_news_type` method.
    """
    if instance.is_public:
        Entry.objects.create(
            object_id=instance._id,
            news_type=instance.get_news_type(),
            sender=instance.user
        )


@receiver(star_done)
def create_star_entry(instance, user, **kwargs):
    """
    Creates news entry for document stargazers.

    Actually, there is a no model for stargazers.
    It's just an array that holds starred user ids on the document model.

    For that reason, `star_done` signals provides `user` parameter.
    """
    Entry.objects.create(
        object_id=instance._id,
        news_type=NEWS_TYPE_STAR,
        sender=user
    )


@receiver(follow_done)
def create_following_entry(follower, following, **kwargs):
    """
    Creates news entry for following actions.
    """
    Entry.objects.create(
        object_id=following.id,
        news_type=NEWS_TYPE_FOLLOWING,
        sender=follower,
        related_object=dict(username=following.username,
                            email=following.email)
    )


@receiver(follow_done)
def add_to_recipients(follower, following, **kwargs):
    """
    Adds the entries of followed profile to follower's newsfeed.
    """
    Entry.objects.add_to_recipients(
        following=following, follower=follower)


@receiver(unfollow_done)
def remove_from_recipients(follower, following, **kwargs):
    """
    Removes the entries of unfollowed profile.
    """
    Entry.objects.remove_from_recipients(following=following,
                                         follower=follower)


@receiver(comment_delete)
@receiver(document_delete)
@receiver(fork_delete)
def remove_news_entry(instance, **kwargs):
    Entry.objects.delete(
        object_type=instance.get_news_type(),
        object_id=instance._id
    )


@receiver(post_save, sender=User)
def create_registration_entry(instance, created, **kwargs):
    if created:
        Entry.objects.create(
            object_id=instance.id,
            news_type=NEWS_TYPE_REGISTRATION,
            sender=instance,
            related_object=dict(username=instance.username,
                                email=instance.email),
            recipients=[]
        )
