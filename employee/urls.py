from django.http.response import HttpResponseRedirectBase
from django.urls import path

urlpatterns = [
    path('', HttpResponseRedirectBase, name='index')
]

