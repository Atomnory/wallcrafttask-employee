import django_filters
from django.db import models
from django import forms
from .models import Employee, Department


class EmployeeFilter(django_filters.FilterSet):
    class Meta:
        model = Employee
        fields = {
            'department': ['exact'],
            'job_end_date': ['isnull']
        }
        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelChoiceFilter,
                'extra': lambda f: {
                    'lookup_expr': 'exact',
                    'empty_label': 'Все отделы',
                    'label': 'Отдел:',
                    'queryset': Department.objects.all()
                }
            },
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'label': 'Работает в компании:'
                }
            }
        }