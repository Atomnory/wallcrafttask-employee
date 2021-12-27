"""
    URLs of employee application
"""
from django.urls import path
from .views import EmployeeFilterListView, EmployeeDetailView, AlphabeticalEmployeeListView, AlphabeticalNameListView

urlpatterns = [
    path('', EmployeeFilterListView.as_view(), name='index'),
    path('<int:pk>', EmployeeDetailView.as_view(), name='employee'),
    path('alphabetical', AlphabeticalEmployeeListView.as_view(), name='alphabetical'),
    path('<str:letter>', AlphabeticalNameListView.as_view(), name='alphabet_list')
]
