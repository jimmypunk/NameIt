from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^word_profile/(?P<word>[a-zA-Z][_a-zA-Z0-9]+)', views.word_profile, name='word_profile'),
]
