from django import forms
from .models import Ressource

class RessourceForm(forms.ModelForm):
    class Meta:
        model = Ressource
        fields = ['title', 'type', 'is_private']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm'
            }),
            'type': forms.Select(attrs={
                'class': 'block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-teal-500 focus:border-teal-500 sm:text-sm'
            }),
            'is_private': forms.CheckboxInput(attrs={
                'class': 'h-4 w-4 text-teal-600 focus:ring-teal-500 border-gray-300 rounded'
            }),
        }
        labels = {
            'is_private': 'Rendre cette ressource privée (visible uniquement par vos amis)',
        }