from django import forms
from common_data.forms import BootstrapMixin
from . import models 
from django.contrib.auth.models import User

class ConfigForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        model = models.PlannerConfig
        fields = "__all__"

class EventForm(forms.ModelForm, BootstrapMixin):
    owner = forms.ModelChoiceField(
        User.objects.all(), 
        widget=forms.HiddenInput
        )
    class Meta:
        model = models.Event
        exclude = ["participants", 'completed', 'completion_time']