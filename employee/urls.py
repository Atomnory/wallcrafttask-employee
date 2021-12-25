"""
    URLs of employee application
"""
from django.urls import path
from .views import EmployeeFilterListView, EmployeeDetailView

urlpatterns = [
    path('', EmployeeFilterListView.as_view(), name='index'),
    path('<int:pk>', EmployeeDetailView.as_view(), name='employee')
]
