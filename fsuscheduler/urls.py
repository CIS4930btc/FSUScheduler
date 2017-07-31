"""fsuscheduler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from .views import HomePageView
from .views import RegisterView, LoginView, LogoutView
from .views import AddClassView
from .views import ProfileView, ProfileFinalsView, ProfileClassesView

urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),

    url(r'^user/login/$', LoginView.as_view(), name='login'),
    url(r'^user/register/$', RegisterView.as_view(), name='register'),
    url(r'^user/logout/$', LogoutView.as_view(), name='logout'),
    url(r'^user/profile/$', ProfileView.as_view(), name='profile'),
    url(r'^user/profile/classes/$', ProfileClassesView.as_view(), name='profile_classes'),
    url(r'^user/profile/finals/$', ProfileFinalsView.as_view(), name='profile_finals'),
    url(r'^user/add-class/$', AddClassView.as_view(), name='add_class'),

    url(r'^admin/', admin.site.urls),
]
