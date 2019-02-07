# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime 

from django.db import models
from django.db.models import Q
from common_data.utilities import time_choices
from functools import reduce
from decimal import Decimal as D

class WorkOrderRequest(models.Model):
    invoice_type = models.PositiveSmallIntegerField(choices=[
        (0, 'Service Invoice'),
        (1, 'Combined Invoice')
    ])
    service_invoice = models.ForeignKey('invoicing.serviceinvoice', 
        blank=True, null=True, on_delete=models.SET_NULL)
    combined_invoice = models.OneToOneField('invoicing.combinedinvoice',
        blank=True, null=True, on_delete=models.SET_NULL)
    service = models.OneToOneField('services.service', null=True, 
        on_delete=models.SET_NULL)
    status = models.CharField(max_length=16, choices=[
        ('request', 'Requested'),
        ('in-progress', 'In Progress'),
        ('completed', 'Completed'),
        ])


    def update_status(self):
        if self.work_orders.count() > 0:
            self.status = "in-progress"

        completed=True 
        for wo in self.work_orders:
            if not wo.status in ['completed', 'authorized']:
                completed=False

        if completed:
            self.status = 'completed'
        
        self.save()


    @property
    def invoice(self):
        return self.service_invoice if self.invoice_type == 0 else \
            self.combined_invoice

    @property
    def work_orders(self):
        return self.serviceworkorder_set.all()

class ServiceWorkOrder(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('progress', 'In progress'),
        ('completed', 'Completed'),
        ('authorized', 'Authorized'),
        ('declined', 'Declined')
        ]
    date = models.DateField()
    time = models.TimeField(choices = time_choices(
        '06:00:00', '18:30:00', '00:30:00'
        ))
    # for services done within the organization
    internal = models.BooleanField(default=False)
    
    works_request = models.ForeignKey('services.workorderrequest', 
        blank=True, null=True, on_delete=models.SET_NULL)

    description = models.TextField(blank=True, default="")
    completed = models.DateTimeField(null=True, blank=True)
    expected_duration = models.DurationField(choices = time_choices(
        '00:00:00', '08:00:00', '00:30:00', delta=True
        ), null=True, blank=True)
    service_people = models.ManyToManyField('services.ServicePerson', 
        blank=True)
    team = models.ForeignKey('services.ServiceTeam', on_delete=models.SET_NULL, null=True, 
        blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, blank=True)
    authorized_by = models.ForeignKey('employees.Employee', 
        on_delete=models.CASCADE, null=True, 
        blank=True,
        limit_choices_to=Q(user__isnull=False))#filter queryset
    notes = models.ManyToManyField('common_data.note')
    progress = models.CharField(max_length=512, blank=True, default="")

    def __str__(self):
        return "WO{}".format(self.pk) #TODO string padding

    @property
    def procedure_pk(self):
        return self.works_request.service.procedure.pk

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.works_request.update_status()

    @property
    def number_of_employees(self):
        direct = self.service_people.all().count()
        team = 0
        if self.team:
            team = self.team.members.all().count()
    
        return direct + team

    @property
    def expenses(self):
        return self.workorderexpense_set.all()

    @property 
    def time_logs(self):
        # may decide to remove the filter and use .all()
        return self.timelog_set.filter(employee__uses_timesheet=True)

    @property
    def progress_list(self):
        pl = self.progress.split(",") if self.progress != "" else []
        return [ int(i) for i in  pl]

    @property
    def progress_percentage(self):
        if not self.works_request.service.procedure or \
                self.works_request.service.procedure.steps.count() ==0:
            return 100 
        

        total_steps = self.works_request.service.procedure.steps.count()
        progress = len(self.progress_list)

        return int(float(progress) * 100.0/ float(total_steps))
        

    @property
    def total_normal_time(self):
        return reduce(lambda x, y: x + y, [i.normal_time \
                for i in self.time_logs], datetime.timedelta(seconds=0))
    
    @property
    def total_overtime(self):
        return reduce(lambda x, y: x + y,
            [i.overtime for i in self.time_logs], datetime.timedelta(seconds=0))

class TimeLog(models.Model):
    work_order = models.ForeignKey('services.serviceworkorder', null=True, 
        on_delete=models.SET_NULL)
    employee = models.ForeignKey('employees.employee', null=True, 
        on_delete=models.SET_NULL)
    date = models.DateField(default=datetime.date.today)
    normal_time = models.DurationField()
    overtime = models.DurationField()
    #using fields to perserve the cost in case the paygrade changes
    normal_time_cost = models.DecimalField(max_digits=8, decimal_places=2, 
        default=D(0.0))
    overtime_cost = models.DecimalField(max_digits=8, decimal_places=2,
        default=D(0.0))

    @property
    def total_cost(self):
        return self.normal_time_cost + self.overtime_cost

    def save(self, *args, **kwargs):
        if not self.pk:
            self.normal_time_cost = D(self.employee.pay_grade.hourly_rate) * \
                self.normal_time.seconds / 3600
            self.overtime_cost = D(self.employee.pay_grade.overtime_rate) * \
                self.overtime.seconds / 3600

        super().save(*args, **kwargs)



class WorkOrderExpense(models.Model):
    work_order = models.ForeignKey('services.ServiceWorkOrder', 
        on_delete=models.SET_NULL, null=True) 
    expense = models.ForeignKey('accounting.Expense', 
        on_delete=models.SET_NULL, null=True)
