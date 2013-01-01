from datetime import datetime
from bson import ObjectId
from django.db import models
from django.dispatch import receiver

from comments.models import Comment
from comments.signals import comment_done
from documents import signals, get_collection
from documents.models import Document
from documents.signals import document_done, fork_done, star_done
from newsfeed.constants import NEWS_TYPE_COMMENT, NEWS_TYPE_DOCUMENT, NEWS_TYPE_FORK, NEWS_TYPE_STAR, NEWS_TYPE_FOLLOWING
from profiles.management.signals import follow_done

RELATED_MODELS = {
    NEWS_TYPE_COMMENT: Comment,
    NEWS_TYPE_DOCUMENT: Document,
    NEWS_TYPE_FORK: Document,
    NEWS_TYPE_STAR: Document
}

class Entry(dict):
    """
    A model that wraps mongodb document
    """
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
    newsfeed = get_collection("newsfeed")
    newsfeed.insert({
        "object_id": instance._id,
        "news_type": instance.get_news_type(),
        "date_created": instance.date_created,
        "user": {
            "username": instance.user.username,
            "email": instance.user.email # it's required for gravatar
        },
    })

@receiver(star_done)
def create_star_entry(instance, user, **kwargs):
    newsfeed = get_collection("newsfeed")
    newsfeed.insert({
        "object_id": instance._id,
        "news_type": NEWS_TYPE_STAR,
        "date_created": datetime.now(),
        "user": {
            "username": user.username,
            "email": user.email # it's required for gravatar
        },
    })

@receiver(follow_done)
def create_following_entry(follower, following, **kwargs):
    newsfeed = get_collection("newsfeed")
    newsfeed.insert({
        "object_id": following.id,
        "news_type": NEWS_TYPE_FOLLOWING,
        "date_created": datetime.now(),
        "related_object": {
            "username": following.username,
            "email": following.email
        },
        "user": {
            "username": follower.username,
            "email": follower.email # it's required for gravatar
        },
    })