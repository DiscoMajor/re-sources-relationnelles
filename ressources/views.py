from django.shortcuts import render
from django.views.generic import CreateView, DeleteView
from django.urls import reverse_lazy
from .models import Ressource
from comments.models import Comment
from .forms import RessourceForm
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils import timezone


class RessourceDetailView(DetailView):
    model = Ressource
    template_name = 'ressources/ressource-detail.html'
    context_object_name = 'ressource'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(
            ressource=self.object, 
            is_deleted=False
        ).order_by('-created_at')
        context['comment_form'] = CommentForm()
        return context


class RessourceListView(ListView):
    model = Ressource
    template_name = 'ressources/ressource-list.html'
    context_object_name = 'ressources'
    
    def get_queryset(self):
        base_queryset = Ressource.objects.filter(deleted_at__isnull=True)
        if self.request.user.is_authenticated:
            own_resources = base_queryset.filter(author=self.request.user)
            public_resources = base_queryset.filter(is_private=False)
            
            if hasattr(self.request.user, 'amis'):
                friends_ids = self.request.user.amis.values_list('id', flat=True)
                friends_private_resources = base_queryset.filter(
                    is_private=True, 
                    author__id__in=friends_ids
                )
                return (own_resources | public_resources | friends_private_resources).distinct()
            
            return (own_resources | public_resources).distinct()
        
        return base_queryset.filter(is_private=False)
    

class RessourceCreateView(LoginRequiredMixin, CreateView):
    model = Ressource
    form_class = RessourceForm
    template_name = 'ressources/ressource-form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse_lazy('ressources:list')
    
class RessourceDeleteView(LoginRequiredMixin, DeleteView):
    model = Ressource
    template_name = 'ressources/ressource-confirm-delete.html'

    def get_queryset(self):
        return Ressource.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.deleted_at = timezone.now()
        self.object.save()

        return redirect('ressources:list')