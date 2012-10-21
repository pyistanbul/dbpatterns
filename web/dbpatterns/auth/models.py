from django.contrib.auth.models import AnonymousUser

class AnonymousProfile(AnonymousUser):
    username = "AnonymousUser"