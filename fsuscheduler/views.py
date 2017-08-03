# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .forms import RegistrationForm, LoginForm, AddClassForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import ContextMixin
from braces import views
from finals.models import Final
from .scheduleRetriever import get_exam_info, get_specific_final
from django.contrib import messages
from django.views.generic import TemplateView

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
class AddClassView(views.LoginRequiredMixin,
                   views.FormValidMessageMixin,
                   views.FormInvalidMessageMixin,
                   generic.CreateView):
    form_class = AddClassForm
    template_name = 'user/add_class.html'
    form_valid_message = "The information you entered has been added to your class list."
    form_invalid_message = "We couldn't find that class."
    success_url = reverse_lazy('profile')
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
            return self.form_invalid(form)

        form.instance.final_info = result;
        form.instance.user_name = self.request.user
        return super(AddClassView, self).form_valid(form)

class ProfileView(views.LoginRequiredMixin,
                  generic.TemplateView):
    template_name = "user/profile.html"

#Bethany Sanders
class ProfileFinalsView(views.LoginRequiredMixin,
                        generic.TemplateView):
        template_name = 'user/finals.html'
        model = Final

        def get_context_data(self, *args, **kwargs):
            context = super(ProfileFinalsView, self).get_context_data(*args, **kwargs)
            context['ngapp'] = "fsuscheduler"
            context['query_results'] = self.get_queryset()
            return context

        def get_queryset(self):
            query_results = Final.objects.all().filter(user_name = self.request.user)
            return query_results

class ProfileClassesView(views.LoginRequiredMixin,
                         generic.TemplateView):
        template_name = 'user/classes.html'
        model = Final

        def get_context_data(self, *args, **kwargs):
            context = super(ProfileClassesView, self).get_context_data(*args, **kwargs)
            context['classes'] = self.get_classes()
            return context

        def get_classes(self):
            classes = Final.objects.all().filter(user_name = self.request.user)
            for c in classes:
                time = str(getattr(c, 'class_time'))
                time = time[:-3]
                setattr(c, 'class_time', time)
            return classes

def DeleteClassView(request, classId):
    classToDelete = get_object_or_404(Final, pk=classId)
    if getattr(classToDelete, 'user_name_id') is request.user.id:
        classToDelete.delete()
    return HttpResponseRedirect(reverse_lazy('profile_classes'))
