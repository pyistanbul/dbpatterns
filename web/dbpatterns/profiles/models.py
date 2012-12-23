from django.db import models
from django.contrib.auth.models import AnonymousUser, User
from django.dispatch import receiver
from django.utils.encoding import smart_unicode


class AnonymousProfile(AnonymousUser):
    username = "AnonymousUser"
    email = ""

    def get_full_name(self):
        return self.username


class Profile(models.Model):
    """
    Extra information for the user model of django.
    """
    user = models.ForeignKey(User)
    following = models.ManyToManyField("self",
                    symmetrical=False, related_name="followers")

    def __unicode__(self):
        return smart_unicode(self.user.username)


@receiver(models.signals.post_save, sender=User)
def create_profile(instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)