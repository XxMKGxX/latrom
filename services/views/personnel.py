import os
import json
import urllib

from django.urls import reverse_lazy 
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView
from rest_framework.viewsets import ModelViewSet
from services import models
from services import forms
from services import filters 
from services import serializers
from common_data.utilities import ExtraContext
from django_filters.views import FilterView

####################################################
#                Service Employees                 #
####################################################
class ServicePersonCreateView(ExtraContext, CreateView):
    template_name = os.path.join('common_data', 'create_template.html')
    form_class = forms.ServicePersonForm
    success_url = reverse_lazy('services:service-person-list')
    extra_context = {
        'title': 'Add Employee to Service Personnel'
    }

class ServicePersonUpdateView(ExtraContext, UpdateView):
    template_name = os.path.join('common_data', 'create_template.html')
    form_class = forms.ServicePersonForm
    success_url = reverse_lazy('services:service-person-list')
    model = models.ServicePerson
    extra_context = {
        'title': 'Update Service Person Details'
    }

class ServicePersonListView(ExtraContext, FilterView):
    template_name = os.path.join('services', 'personnel', 'list.html')
    queryset = models.ServicePerson.objects.all()
    extra_context = {
        'title': 'Service Personnel List',
        'new_link': reverse_lazy('services:service-person-create')
    }
    filterset_class = filters.ServicePersonFilter

class ServicePersonDashboardView(DetailView):
    template_name = os.path.join('services', 'personnel', 'dashboard.html')
    model = models.ServicePerson

####################################################
#                    Service Teams                 #
####################################################
class ServiceTeamCRUDMixin(object):
    def post(self, request, *args, **kwargs):
        update_flag = isinstance(self, UpdateView)
        resp = super(ServiceTeamCRUDMixin, self).post(request, *args, **kwargs)
        if not self.object:
            return resp 
        
        if update_flag:
            self.object.members.clear()
        
        members_list = json.loads(urllib.unquote(request.POST['members']))
        for data in members_list:
            pk = data['value'].split('-')[0]
            service_person = models.ServicePerson.objects.get(pk=pk)
            self.object.members.add(service_person)

        return resp

class ServiceTeamCreateView(ServiceTeamCRUDMixin, CreateView):
    template_name = os.path.join('services', 'personnel', 'teams', 
        'create.html')
    form_class = forms.ServiceTeamForm
    success_url = reverse_lazy('services:team-list')

    

class ServiceTeamUpdateView(ServiceTeamCRUDMixin, UpdateView):
    template_name = os.path.join('services', 'personnel', 'teams', 
        'update.html')
    form_class = forms.ServiceTeamForm
    success_url = reverse_lazy('services:team-list')
    model = models.ServiceTeam

class ServiceTeamDetailView(DetailView):
    template_name = os.path.join('services', 'personnel', 'teams', 
        'detail.html')
    model = models.ServiceTeam

class ServiceTeamListView(ExtraContext, ListView):
    template_name = os.path.join('services', 'personnel', 'teams', 
        'list.html')
    queryset = models.ServiceTeam.objects.all()
    extra_context = {
        'title': 'List of Service Teams',
        'new_link': reverse_lazy('services:team-create')
    }

class ServiceTeamAPIView(ModelViewSet):
    serializer_class = serializers.ServiceTeamSerializer
    queryset = models.ServiceTeam.objects.all()

class ServicePersonAPIView(ModelViewSet):
    serializer_class = serializers.ServicePersonSerializer
    queryset = models.ServicePerson.objects.all()