from django.contrib.auth.models import AnonymousUser

class AnonymousProfile(AnonymousUser):
    username = "AnonymousUser"
    email = ""

    def get_full_name(self):
        return self.username