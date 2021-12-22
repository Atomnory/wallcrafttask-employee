from django.db import models
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Employee


class EmployeeListView(ListView):
    model = Employee
    paginate_by = 20


class EmployeeDetailView(DetailView):
    model = Employee


class AlphabeticalEmployeeListView(ListView):
    pass
