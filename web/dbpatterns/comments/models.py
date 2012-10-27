from bson import ObjectId

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from gravatar.templatetags.gravatar import gravatar_for_email
from auth.models import AnonymousProfile
from documents import get_collection
from documents.models import Document

class Comment(dict):
    # dictionary-like object for mongodb documents.
    __getattr__ = dict.get

    @property
    def profile_url(self):
        return reverse("auth_profile", args=[self.user.username])

    @property
    def avatar_url(self):
        return gravatar_for_email(self.user.email, size=40)

    @property
    def username(self):
        return self.user.username

    @property
    def full_name(self):
        return self.user.get_full_name() or None

    @property
    def user(self):
        if not self._cached_user:
            self._cached_user = self.get_user()

        return self._cached_user

    def get_user(self):
        try:
            return User.objects.get(id=self.user_id)
        except User.DoesNotExist:
            return AnonymousProfile()

    @property
    def document(self):
        return Document(get_collection("documents").find_one({
            "_id": ObjectId(self.document_id)
        }))