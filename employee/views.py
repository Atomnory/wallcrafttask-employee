from django.views.generic import ListView, DetailView
from .models import Employee
from .filters import EmployeeFilter
from django_filters.views import FilterView
from .services import get_employees_by_last_name_group, AlphabeticalGrouper
from typing import Dict, Any


class EmployeeFilterListView(FilterView):
    template_name = 'employee/employee_list.html'
    model = Employee
    paginate_by = 15
    filterset_class = EmployeeFilter


class EmployeeDetailView(DetailView):
    model = Employee


class AlphabeticalEmployeeListView(ListView):
    template_name = 'employee/alphabetical_employee_list.html'
    context_object_name = 'groups'

    def get_queryset(self):
        result_groups = AlphabeticalGrouper.get_alphabetical_groups()
        self.request.session['result_groups'] = result_groups
        return result_groups


class AlphabeticalNameListView(ListView):
    template_name = 'employee/alphabetical_employee_list.html'
    context_object_name = 'employees'
    # TODO: fix template when in groups only one letter
    def get_queryset(self):
        self.groups = self.request.session.get('result_groups')
        return get_employees_by_last_name_group(self.groups, self.kwargs.get('letter'))

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['groups'] = self.groups
        return context
