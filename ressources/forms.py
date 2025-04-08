from django import forms
from .models import Ressource

class RessourceForm(forms.ModelForm):
    class Meta:
        model = Ressource
        fields = ['title', 'type', 'relation']
        widgets = {
            'relation': forms.CheckboxSelectMultiple(),
        }