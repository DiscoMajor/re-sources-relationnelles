from django.shortcuts import render

from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Ressource
from .forms import RessourceForm
from django.contrib.auth.mixins import LoginRequiredMixin

class RessourceCreateView(LoginRequiredMixin, CreateView):
    model = Ressource
    form_class = RessourceForm
    template_name = 'ressources/ressource-form.html'

    def get_success_url(self):
        return reverse_lazy('ressources:add')