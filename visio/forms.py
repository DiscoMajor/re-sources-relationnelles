from datetime import datetime
from django import forms
from .models import Meeting


class MeetingCreateForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ["title_of_meeting", "starting_date_time", "duration"]
        widgets = {
            "title_of_meeting": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom de la réunion..."
            }),
            "starting_date_time": forms.DateTimeInput(attrs={
                "class": "form-control flatpickr",
                "data-enable-time": "true",
                "data-time_24hr": "true",
                "data-min-date": "today"
            }),
            "duration": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Durée de la réunion en minutes..."
            }),
        }