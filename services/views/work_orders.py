import os 
import json 
import urllib

from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic import ListView ,TemplateView, DetailView
from django.views.generic.edit import CreateView, UpdateView
from services import models
from services import forms 
from services import filters
from services import serializers
from common_data.utilities import ExtraContext
from django_filters.views import FilterView
from rest_framework.viewsets import ModelViewSet

class WorkOrderCRUDMixin(object):
    def post(self, request, *args, **kwargs):
        update_flag = isinstance(self, UpdateView)
        resp = super(WorkOrderCRUDMixin, self).post(request, *args, **kwargs)
        if not self.object:
            return resp
        service_people = json.loads(urllib.unquote(
            request.POST['service_people']))
        
        if update_flag:
            self.object.service_people.clear()

        for sp in service_people:
            pk = sp['value'].split('-')[0]
            service_person = models.ServicePerson.objects.get(pk=pk)
            self.object.service_people.add(service_person)

        return resp



class WorkOrderCreateView(WorkOrderCRUDMixin, CreateView):
    template_name = os.path.join('services', 'work_order', 'create.html')
    form_class = forms.ServiceWorkOrderForm
    success_url = reverse_lazy('services:work-order-list')

    def get_initial(self):
        return {
            'status': 'requested'
        }

    
class WorkOrderUpdateView(WorkOrderCRUDMixin, UpdateView):
    template_name = os.path.join('services', 'work_order', 'update.html')
    form_class = forms.ServiceWorkOrderForm
    success_url = reverse_lazy('services:work-order-list')
    model = models.ServiceWorkOrder


class WorkOrderCompleteView(UpdateView):
    template_name = os.path.join('services', 'work_order', 'complete.html')
    form_class = forms.ServiceWorkOrderCompleteForm
    success_url = reverse_lazy('services:work-order-list')
    model = models.ServiceWorkOrder

    def get_initial(self):
        return {
            'status': 'requested'
        }


class WorkOrderDetailView(DetailView):
    template_name = os.path.join('services', 'work_order', 'detail.html')
    model = models.ServiceWorkOrder

    def get_context_data(self, *args, **kwargs):
        context = super(WorkOrderDetailView, self).get_context_data(
            *args, **kwargs)
        # provide initial data for this form
        context['authorization_form'] = forms.ServiceWorkOrderAuthorizationForm(
            
        )
        return context

class WorkOrderListView(ExtraContext, FilterView):
    template_name = os.path.join('services', 'work_order', 'list.html')
    filterset_class = filters.WorkOrderFilter
    queryset = models.ServiceWorkOrder.objects.all()
    extra_context = {
        'title': 'List of Work Orders',
        'new_link': reverse_lazy('services:work-order-create')
    }


class WorkOrderViewSet(ModelViewSet):
    serializer_class = serializers.WorkOrderSerializer
    queryset = models.ServiceWorkOrder.objects.all()


def work_order_authorize(request, pk=None):
    worder = get_object_or_404(models.ServiceWorkOrder, pk=pk)
    form = forms.ServiceWorkOrderAuthorizationForm(request.POST)
    if form.is_valid():
        worder.status = form.cleaned_data['status']
        worder.authorized_by = form.cleaned_data['authorized_by']
        worder.save()
    else: return HttpResponse(reverse_lazy(request.path))
    return HttpResponseRedirect(reverse_lazy('services:work-order-list'))