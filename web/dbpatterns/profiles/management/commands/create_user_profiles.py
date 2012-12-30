from django.contrib.auth.models import User
from django.core.management import BaseCommand

from profiles.models import Profile


class Command(BaseCommand):
    """
    A migration command that creates profile instances
    for django's user model.
    """
    def handle(self, *args, **options):

        Profile.objects.all().delete()

        for user in User.objects.all():
            Profile.objects.get_or_create(user=user)