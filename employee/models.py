from django.db import models
from django.urls import reverse


class Department(models.Model):
    name = models.CharField(verbose_name='Department name', max_length=80, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self) -> str:
        return str(self.name)


class Employee(models.Model):
    first_name = models.CharField(verbose_name="First name", max_length=40)
    last_name = models.CharField(verbose_name='Last name', max_length=40)
    patronymic_name = models.CharField(verbose_name='Patronymic name', max_length=40, blank=True)
    birth_date = models.DateField(verbose_name='Birth date')
    email = models.EmailField(verbose_name='Email', max_length=100, unique=True)
    phone_number = models.CharField(verbose_name='Phone number', max_length=20, unique=True)
    job_start_date = models.DateField(verbose_name='Job start date')
    job_end_date = models.DateField(verbose_name='Job end date', null=True, blank=True)
    job_title = models.CharField(verbose_name='Job title', max_length=40)
    department = models.ForeignKey(to=Department, on_delete=models.PROTECT, verbose_name='Department')

    class Meta:
        ordering = ['pk']
        
    def __str__(self) -> str:
        return '%s %s' % (self.first_name, self.last_name)
    
    def get_absolute_url(self) -> str:
        return reverse('employee', kwargs={"pk": self.pk})
    
    def get_full_name(self) -> str:
        return '%s %s %s' % (self.first_name, self.patronymic_name, self.last_name)
