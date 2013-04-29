from bson import ObjectId

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from gravatar.templatetags.gravatar import gravatar_for_email
from newsfeed.constants import NEWS_TYPE_COMMENT

from profiles.models import AnonymousProfile
from documents import get_collection
from documents.models import Document


class CommentManager(object):
    def get(self, **kwargs):
        return Comment(get_collection("comments").find_one(kwargs))


class Comment(dict):
    """
    A model that allows create, read comments from mongodb
    """
    __getattr__ = dict.get
    objects = CommentManager()

    @property
    def profile_url(self):
        """Return profile url of user"""
        return reverse("auth_profile", args=[self.user.username])

    @property
    def avatar_url(self):
        """Returns the gravar address of email"""
        return gravatar_for_email(self.user.email, size=40)

    @property
    def username(self):
        """Shortcut parameter to username"""
        return self.user.username

    @property
    def full_name(self):
        """Shortcut parameter to full name"""
        return self.user.get_full_name() or None

    @property
    def user(self):
        """Returns cached user"""
        if not self._cached_user:
            self._cached_user = self.get_user()

        return self._cached_user

    def get_user(self):
        """Returns the user of comment"""
        try:
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return AnonymousProfile()

    @property
    def document(self):
        """Returns the document of comment"""
        query = {"_id": ObjectId(self.document_id)}
        return Document(get_collection("documents").find_one(query))

    @property
    def pk(self):
        """Shortcut method to deal with underscore restriction
        of django templates"""
        return self._id

    def get_news_type(self):
        """Returns newsfeed type."""
        return NEWS_TYPE_COMMENT

    @property
    def is_public(self):
        """Returns the visibility of the document of comment"""
        return self.document.is_public