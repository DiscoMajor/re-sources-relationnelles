from django.shortcuts import render

from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Comment
from ressources.models import Ressource
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string

class CommentListView(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'comments/comment-list.html'
    context_object_name = 'comments'

    def get_queryset(self):
        ressource = get_object_or_404(Ressource, pk=self.kwargs['ressource_pk'])
        return Comment.objects.filter(ressource=ressource, is_deleted=False).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ressource'] = get_object_or_404(Ressource, pk=self.kwargs['ressource_pk'])
        return context


class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment-form.html'

    def form_valid(self, form):
        ressource = get_object_or_404(Ressource, pk=self.kwargs['ressource_pk'])
        form.instance.citoyen = self.request.user
        form.instance.ressource = ressource
        self.object = form.save()

        if self.request.headers.get('Turbo-Frame'):
            comments = Comment.objects.filter(
                ressource=ressource, is_deleted=False
            ).order_by('-created_at')
            html = render_to_string('comments/_comment_list.html',{
                'comments': comments, 'ressource': ressource
            },
            request=self.request
            )
            return HttpResponse(html)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ressources:detail', kwargs={'pk': self.object.ressource.pk})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'comments/comment-form.html'

    def get_queryset(self):
        return Comment.objects.filter(citoyen=self.request.user, is_deleted=False)

    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get('Turbo-Frame'):
            comments = Comment.objects.filter(
                ressource=self.object.ressource, is_deleted=False
            ).order_by('-created_at')
            html = render_to_string(
                'comments/_comment_list.html',
                {'comments': comments, 'ressource': self.object.ressource},
                request=self.request
            )
            return HttpResponse(html)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('ressources:detail', kwargs={'pk': self.object.ressource.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = 'comments/comment-confirm-delete.html'

    def get_queryset(self):
        return Comment.objects.filter(citoyen=self.request.user, is_deleted=False)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.save()

        if self.request.headers.get('Turbo-Frame'):
            comments = Comment.objects.filter(
                ressource=self.object.ressource, is_deleted=False
            ).order_by('-created_at')
            html = render_to_string(
                'comments/_comment-list.html',
                {'comments': comments, 'ressource': self.object.ressource},
                request=self.request
            )
            return HttpResponse(html)

        return redirect('ressources:detail', pk=self.object.ressource.pk)