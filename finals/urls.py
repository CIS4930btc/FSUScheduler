from django.conf.urls import url

from . import views
from .views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='finals'),
]
