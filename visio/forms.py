from django import forms
from .models import Meeting


class MeetingCreateForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ["title_of_meeting", "starting_date_time", "duration", ]
        labels = {
            "title_of_meeting": "Nom de la Réunion",
            "starting_date_time": "Date et Heure de Début",
            "duration": "Durée (minutes)",
        }

        widgets = {
            "title_of_meeting": forms.TextInput(attrs={"class": "form-control", "placeholder":
                "Nom de la réunion..."}),
            "starting_date_time": forms.DateTimeInput(attrs={"class": "form-control date"}),
            "duration": forms.NumberInput(attrs={"class": "form-control", "placeholder":
                "Durée de la réunion en minutes..."}),
        }
