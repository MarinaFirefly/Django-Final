from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, FormView, ListView, DeleteView, TemplateView, View, UpdateView

from authentication.forms import RegistrationForm


class Registration(CreateView):
    form_class = RegistrationForm
    template_name = 'registration.html'
    success_url = '../login/'


class Login(LoginView):
    http_method_names = ['get', 'post']
    template_name = 'login.html'


class Logout(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect("/")

