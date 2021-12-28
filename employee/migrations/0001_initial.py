# Generated by Django 4.0 on 2021-12-22 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, unique=True, verbose_name='Department name')),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40, verbose_name='First name')),
                ('last_name', models.CharField(max_length=40, verbose_name='Last name')),
                ('patronymic_name', models.CharField(blank=True, max_length=40, verbose_name='Patronymic name')),
                ('birth_date', models.DateField(verbose_name='Birth date')),
                ('email', models.EmailField(max_length=100, unique=True, verbose_name='Email')),
                ('phone_number', models.CharField(max_length=20, unique=True, verbose_name='Phone number')),
                ('job_start_date', models.DateField(verbose_name='Job start date')),
                ('job_end_date', models.DateField(blank=True, null=True, verbose_name='Job end date')),
                ('job_title', models.CharField(max_length=40, verbose_name='Job title')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='employee.department', verbose_name='Department')),
            ],
        ),
    ]
