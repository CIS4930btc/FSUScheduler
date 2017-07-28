# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .forms import RegistrationForm, LoginForm, FinalForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import ContextMixin
from braces import views
from finals.models import Final
from .scheduleRetriever import get_exam_info, get_specific_final
from django.contrib import messages

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

#Bethany Sanders
class FinalView(views.LoginRequiredMixin,
                views.FormValidMessageMixin,
                generic.CreateView):
    form_class = FinalForm
    template_name = 'user/final.html'
    form_invalid_message = "We couldn't find that final. Double check your information and try again!"
    form_valid_message = "The information you entered has been added to the database. "
    success_url = reverse_lazy('finals')
    Model = Final

    def form_valid(self, form):
        class_time_format = str(form.instance.class_time)
        if class_time_format[0] == "0":
            class_time_format = class_time_format[1:5]
        else:
            class_time_format = class_time_format[0:5]
        class_time_format += " " + form.instance.class_timeframe

        result = get_specific_final(form.instance.class_semester, form.instance.class_name,
                                    form.instance.class_day, class_time_format)

        if result == "":
            messages.error(self.request, "We couldn't find that final.")
            return self.form_invalid(form)

        form.instance.final_info = result;
        form.instance.user_name = self.request.user
        return super(FinalView, self).form_valid(form)
