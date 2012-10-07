from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.views.generic import FormView, CreateView, TemplateView, RedirectView, DetailView

from auth.forms import RegistrationForm
from documents.models import Document
from documents.resources import DocumentResource


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
        return reverse("home")

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
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        resource = DocumentResource()
        collection = resource.get_collection().find({"user_id": self.get_object().pk})
        context["documents"] = map(Document, collection)
        return context