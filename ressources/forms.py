from django import forms
from .models import Ressource

class RessourceForm(forms.ModelForm):
    class Meta:
        model = Ressource
        fields = ['title', 'type', 'is_private']
        widgets = {
            'is_private': forms.CheckboxInput(),
        }
        labels = {
                'is_private': 'Rendre cette ressource privée (visible uniquement par vos amis)',
            }