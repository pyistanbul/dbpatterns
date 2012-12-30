from django.db import models
from django.contrib.auth.models import AnonymousUser, User
from django.utils.encoding import smart_unicode


class AnonymousProfile(AnonymousUser):
    username = "AnonymousUser"
    email = ""

    def get_full_name(self):
        return self.username


class FollowedProfile(models.Model):
    """
    A relationship model for following users
    """
    follower = models.ForeignKey(User, related_name="following")
    following = models.ForeignKey(User, related_name="followers")

    def __unicode__(self):
        return smart_unicode("%s following %s" % (self.follower.username,
                                                  self.following.username))