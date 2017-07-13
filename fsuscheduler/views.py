# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .forms import RegistrationForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from braces import views

class HomePageView(generic.TemplateView):
    template_name = "home.html"

class RegisterView(views.AnonymousRequiredMixin, 
                   views.FormValidMessageMixin,
                   generic.CreateView):
    form_class = RegistrationForm
    model = User
    template_name = 'user/register.html'
    success_url = reverse_lazy('login')
    form_valid_message = "You can now login below."

class LoginView(views.AnonymousRequiredMixin,
                views.FormValidMessageMixin,
                generic.FormView):
    form_class = LoginForm
    template_name = 'user/login.html'
    success_url = reverse_lazy('home')
    form_valid_message = "Welcome!"

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            return self.form_invalid(form)

class LogoutView(views.LoginRequiredMixin,
                 views.MessageMixin,
                 generic.RedirectView):
    url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        logout(request)
        self.messages.success("See ya!")
        return super(LogoutView, self).get(request, *args, **kwargs)
