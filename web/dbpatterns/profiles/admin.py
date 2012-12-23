from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from gravatar.templatetags.gravatar import gravatar_for_user

class ProfileAdmin(UserAdmin):

    list_display = ('gravatar', 'username', 'email', 'first_name', 'last_name', 'is_staff')
    ordering = ("-id", )

    def gravatar(self, obj):
        return '<img src="%s" />' % gravatar_for_user(obj)
    gravatar.allow_tags = True

admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)