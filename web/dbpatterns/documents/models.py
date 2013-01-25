from bson import ObjectId

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from newsfeed.constants import NEWS_TYPE_FORK, NEWS_TYPE_DOCUMENT

from profiles.models import AnonymousProfile
from documents import get_collection
from documents.utils import reverse_tastypie_url

class DocumentManager(object):

    def __init__(self):
        self.load()

    def load(self):
        self.collection = get_collection("documents")

    def get(self, **kwargs):
        return Document(self.collection.find_one(kwargs))

    def featured(self):
        return map(Document, self.collection.find({
            "is_featured": True
        }))

    def starred(self, user_id):
        return map(Document, self.collection.find({
            "stars": {
                "$in": [user_id]
            }
        }))


class Document(dict):
    """
    A model that wraps MongoDB document.
    """
    __getattr__ = dict.get
    objects = DocumentManager()

    def __repr__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("show_document", args=[self.pk])

    def get_edit_url(self):
        return reverse("edit_document", args=[self.pk])

    def get_resource_uri(self):
        return reverse_tastypie_url("documents", self.pk)

    def forks(self):
        return map(self.__class__, get_collection("documents").find({
            "fork_of": self.pk
        }))

    def get_user(self):
        try:
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return AnonymousProfile()

    @property
    def user(self):
        if not self._cached_user:
            self._cached_user = self.get_user()

        return self._cached_user

    @property
    def pk(self):
        return self._id

    def get_fork_count(self):
        return self.fork_count or 0

    def get_stars(self):
        return self.stars or []

    @property
    def star_count(self):
        return len(self.get_stars())

    @property
    def comment_count(self):
        return get_collection("comments").find({
            "document_id": self.pk
        }).count()

    def get_stargazers(self):
        return User.objects.filter(id__in=self.get_stars())

    def get_news_type(self):
        if self.fork_of is not None:
            return NEWS_TYPE_FORK
        return NEWS_TYPE_DOCUMENT