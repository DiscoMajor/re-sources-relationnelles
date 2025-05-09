from datetime import datetime
from django import forms
from .models import Meeting


class MeetingCreateForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ["title_of_meeting", "starting_date_time", "duration"]
        labels = {
            "title_of_meeting": "Titre",
            "starting_date_time": "Date et heure de début",
            "duration": "Durée (en minutes)",
        }
        widgets = {
            "title_of_meeting": forms.TextInput(attrs={
                "class": "block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm",
                "placeholder": "Nom de la réunion..."
            }),
            "starting_date_time": forms.DateTimeInput(attrs={
                "class": "block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm flatpickr",
                "data-enable-time": "true",
                "data-time_24hr": "true",
                "data-min-date": "today"
            }),
            "duration": forms.NumberInput(attrs={
                "class": "block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm",
                "placeholder": "Durée de la réunion en minutes..."
            }),
        }