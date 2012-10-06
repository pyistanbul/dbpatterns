from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.views.generic import FormView, CreateView, TemplateView, RedirectView

from auth.forms import RegistrationForm


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
