from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='profile'),
    url(r'^edit/$', views.edit, name='edit_profile'),
]
