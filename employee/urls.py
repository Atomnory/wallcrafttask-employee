from django.http.response import Http404, HttpResponseRedirectBase
from django.urls import path
from .views import EmployeeListView, EmployeeDetailView

urlpatterns = [
    path('', EmployeeListView.as_view(), name='index'),
    path('<int:pk>', EmployeeDetailView.as_view(), name='employee')
]
