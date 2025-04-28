from django import forms

class AddressSearchForm(forms.Form):
    address = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-teal-500',
            'placeholder': 'Rechercher une adresse...',
            'data-address-target': 'input',
            'data-action': 'keydown->address#handleKeyDown'
        })
    )