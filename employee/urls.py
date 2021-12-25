"""
    URLs of employee application
"""
from django.urls import path
from .views import EmployeeFilterListView, EmployeeDetailView, alphabetical_list_view, alpha_list

urlpatterns = [
    path('', EmployeeFilterListView.as_view(), name='index'),
    path('<int:pk>', EmployeeDetailView.as_view(), name='employee'),
    path('alphabetical', alphabetical_list_view, name='alphabetical'),
    path('<str:letter>', alpha_list, name='alpha_list')
]
