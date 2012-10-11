from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from documents import get_collection
from documents.utils import reverse_tastypie_url


class Document(dict):
    """
    A model that wraps MongoDB document.
    """
    __getattr__ = dict.get

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
            return None

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