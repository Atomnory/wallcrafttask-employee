from typing import Dict, Any
from django.views.generic import ListView, DetailView
from django_filters.views import FilterView
from .models import Employee
from .filters import EmployeeFilter
from .services import get_employees_by_last_name_group, AlphabeticalGrouper


class EmployeeFilterListView(FilterView):
    template_name = 'employee/employee_list.html'
    model = Employee
    paginate_by = 15
    filterset_class = EmployeeFilter


class EmployeeDetailView(DetailView):
    model = Employee


class AlphabeticalEmployeeListView(ListView):
    template_name = 'employee/alphabetical_groups.html'
    context_object_name = 'groups'

    def get_queryset(self):
        result_groups = AlphabeticalGrouper().get_alphabetical_groups()
        self.request.session['result_groups'] = result_groups
        return result_groups


class AlphabeticalNameListView(ListView):
    template_name = 'employee/alphabetical_employee_list.html'
    context_object_name = 'employees'
    
    def get_queryset(self):
        self.groups = self.request.session.get('result_groups')
        try:
            return get_employees_by_last_name_group(self.groups, self.kwargs.get('letter'))
        except Exception:
            return None

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['groups'] = self.groups
        return context
