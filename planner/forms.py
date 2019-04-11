from django import forms
from django.contrib.auth.models import User

from common_data.forms import BootstrapMixin

from . import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from crispy_forms.bootstrap import TabHolder, Tab

class ConfigForm(forms.ModelForm, BootstrapMixin):
    class Meta:
        model = models.PlannerConfig
        fields = "number_of_agenda_items",

class EventForm(forms.ModelForm, BootstrapMixin):
    owner = forms.ModelChoiceField(
        User.objects.all(), 
        widget=forms.HiddenInput
        )
    json_participants = forms.CharField(
        widget=forms.HiddenInput
        )
    class Meta:
        model = models.Event
        exclude = ["participants", 'completed', 'completion_time', 'reminder_notification']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            TabHolder(
                Tab('data',
                    Row(
                        Column('date', css_class='form-group col-6'),
                        Column('reminder', css_class='form-group col-6'),
                    ),
                    Row(
                        Column('start_time', css_class='form-group col-6'),
                        Column('end_time', css_class='form-group col-6'),
                    ),
                    Row(
                        Column('label', css_class='form-group col-6'),
                        Column('icon', css_class='form-group col-6'),
                    ),
                    'description',
                    'priority',
                    'repeat',
                    'repeat_active',
                    'owner',
                    'json_participants',
                ),
                Tab('participants',
                    HTML(
                        """
                        <div id="participant-select">
                        </div>
                        """
                    ),
                ),
            )
        )
        self.helper.add_input(Submit('submit', 'Submit'))
