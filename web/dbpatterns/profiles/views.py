from itertools import imap
import json
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import FormView, CreateView, TemplateView, RedirectView, DetailView, ListView

from profiles.forms import RegistrationForm
from documents.models import Document
from documents.resources import DocumentResource
from profiles.management.signals import follow_done


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "auth/register.html"

    def get_success_url(self):
        return reverse("auth_registration_complete")

class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = "auth/login.html"

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        return self.request.GET.get("next") or reverse("home")

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context["next"] = self.request.GET.get("next", "")
        return context


class LogoutView(RedirectView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)

    def get_redirect_url(self, **kwargs):
        return reverse("home")



class ProfileDetailView(DetailView):
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = "profile"
    model = User

    def get_context_data(self, **kwargs):
        user_id = self.get_object().pk
        resource = DocumentResource()

        collection = resource.get_collection().find({
            "user_id": user_id
        })

        followed_by_authenticated_user = self.request.user.following.filter(
                                            following_id=user_id).exists()

        return super(ProfileDetailView, self).get_context_data(
            documents=imap(Document, collection),
            is_followed=followed_by_authenticated_user
        )

    def delete(self, request, **kwargs):
        """
        Removes `FollowedProfile` object for authenticated user.
        """
        user = self.get_object()
        user.followers.filter(follower=request.user).delete()
        return HttpResponse(json.dumps({
            "success": True
        }))

    def post(self, request, **kwargs):
        """
        Creates `FollowedProfile` object for authenticated user.
        """
        user = self.get_object()

        if user.followers.filter(follower=request.user).exists():
            return HttpResponse(json.dumps({
                "error": "You already following this people."
            }))

        user.followers.create(follower=request.user)

        follow_done.send(sender=self,
                        follower=request.user, following=user)

        return HttpResponse(json.dumps({
            "success": True
        }))