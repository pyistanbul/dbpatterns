from bson import ObjectId
from django.db import models
from django.dispatch import receiver

from comments.models import Comment
from comments.signals import comment_done
from documents import signals, get_collection
from documents.models import Document
from documents.signals import document_done, fork_done
from newsfeed.constants import NEWS_TYPE_COMMENT, NEWS_TYPE_DOCUMENT, NEWS_TYPE_FORK

RELATED_MODELS = {
    NEWS_TYPE_COMMENT: Comment,
    NEWS_TYPE_DOCUMENT: Document,
    NEWS_TYPE_FORK: Document
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

        if model:
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



class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=80)

class Restaurant(Place):
    serves_hot_dogs = models.BooleanField()
    serves_pizza = models.BooleanField()

