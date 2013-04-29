from django.contrib.auth.models import User
from django.db.models import Q
from django.views.generic import ListView

from gravatar.templatetags.gravatar import gravatar_for_user

from profiles.mixins import JSONResponseMixin


class UserResource(JSONResponseMixin, ListView):
    queryset = User.objects.all()

    def get_queryset(self):
        keyword = self.request.GET.get("term")
        excludes = self.request.GET.get("excludes", "").split(",")

        if self.request.user.is_authenticated():
            excludes.append(self.request.user.id)

        users = User.objects.filter(
            Q(username__icontains=keyword) |
            Q(email__icontains=keyword) |
            Q(first_name=keyword) | Q(last_name=keyword)
        ).exclude(id__in=filter(bool, excludes))

        return [dict(id=user.id,
                     label=user.username,
                     avatar=gravatar_for_user(user, size=40)) for user in users]

    def render_to_response(self, context, **response_kwargs):
        return super(UserResource, self).render_to_response(
            context.get("object_list"), **response_kwargs)