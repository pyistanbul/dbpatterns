from django.conf.urls import include, patterns, url
from django.views.generic import TemplateView
from auth.views import RegistrationView, LoginView, LogoutView


urlpatterns = patterns('',

    url(r'^login/$', LoginView.as_view(template_name="auth/login.html"),
        name='auth_login'),
    url(r'^logout/$', LogoutView.as_view(), name='auth_logout'),
    url(r'^register/$', RegistrationView.as_view(template_name="auth/register.html"),
        name='auth_registration'),
    url(r'^complete/$', TemplateView.as_view(template_name="auth/complete.html"),
        name='auth_registration_complete'),

)