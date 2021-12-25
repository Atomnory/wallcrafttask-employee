from django.views.generic import ListView, DetailView
from django_filters import filters
from .models import Employee
from .filters import EmployeeFilter
from django.http import request
from django_filters.views import FilterView
from typing import Any, Dict


class EmployeeFilterListView(FilterView):
    template_name = 'employee/employee_list.html'
    model = Employee
    paginate_by = 15
    filterset_class = EmployeeFilter


class EmployeeDetailView(DetailView):
    model = Employee


class AlphabeticalEmployeeListView(ListView):
    pass
