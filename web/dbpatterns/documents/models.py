from pymongo import DESCENDING

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from documents.constants import CAN_EDIT
from newsfeed.constants import NEWS_TYPE_FORK, NEWS_TYPE_DOCUMENT
from profiles.models import AnonymousProfile
from documents import get_collection
from documents.utils import reverse_tastypie_url


class DocumentManager(object):
    """The manager of Document model"""

    def __init__(self):
        self.load()

    def load(self):
        """Reloads mongodb connection"""
        self.collection = get_collection("documents")
        self.collection.ensure_index([
            ("date_created", DESCENDING),
        ])

    def get(self, **kwargs):
        """Returns a single document"""
        return Document(self.collection.find_one(kwargs))

    def assigned(self, user_id):
        """Returns assigned user list"""
        return self.collection.find({
            "assignees.id": {"$in": [user_id]}
        }).sort("date_created", DESCENDING)

    def for_user(self, user_id):
        """Returns documents of the given user id"""
        return self.collection.find({"user_id": user_id}) \
            .sort("date_created", DESCENDING)

    def featured(self):
        """Returns featured documents"""
        return map(Document, self.collection.find({
            "is_featured": True}))

    def starred(self, user_id):
        """Returns starred documents of user"""
        return map(Document, self.collection.find({
            "stars": {"$in": [user_id]}}))


class Document(dict):
    """A model that allows to make CRUD for documents on mongodb"""

    # use dot notation to reach items of dictionary
    # returns none if item is not found
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
        """Returns forks of document"""
        forks = get_collection("documents").find({"fork_of": self.pk})
        return map(Document, forks)

    def get_user(self):
        """Returns the user or anonymous user"""
        try:
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return AnonymousProfile()

    @property
    def user(self):
        """Caches the user"""
        if not self._cached_user:
            self._cached_user = self.get_user()
        return self._cached_user

    @property
    def pk(self):
        """Shortcut method to deal with underscore restriction
        of django templates"""
        return self._id

    def get_fork_count(self):
        """Returns fork count of document"""
        return self.fork_count or 0

    def get_stars(self):
        """Returns starred users or empty list"""
        return self.stars or []

    @property
    def assignees(self):
        """Returns assigned users or empty list"""
        return self.get('assignees') or []

    @property
    def star_count(self):
        """Counts the stargazers"""
        return len(self.get_stars())

    @property
    def comment_count(self):
        """Returns the comment count of document"""
        comments = get_collection("comments")
        return comments.find({"document_id": self.pk}).count()

    def get_stargazers(self):
        """Returns the stargazers of document"""
        return User.objects.filter(id__in=self.get_stars())

    def get_news_type(self):
        """Returns the new type (fork or document) of document"""
        if self.fork_of is not None:
            return NEWS_TYPE_FORK
        return NEWS_TYPE_DOCUMENT

    def is_visible(self, user_id=None):
        """Indicates whether the document is visible to user"""
        assignees = [user.get("id") for user in self.assignees]
        return (self.is_public or
                user_id == self.user_id or
                user_id in assignees)

    def is_editable(self, user_id=None):
        """Indicates the user can edit this document"""
        if user_id == self.user_id:
            return True

        for permission in self.assignees:
            if (permission.get("id") == user_id and
                    permission.get("permission") == CAN_EDIT):
                return True
        return False
