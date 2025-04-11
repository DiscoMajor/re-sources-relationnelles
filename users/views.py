from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from .models import User


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('ressources:list')
    
    def form_invalid(self, form):
        messages.error(self.request, "Identifiants invalides. Veuillez réessayer.")
        return super().form_invalid(form)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'citycode']


class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Compte créé avec succès !")
        return response


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')


@login_required
def profile_view(request):
    """Vue pour afficher et gérer le profil utilisateur"""
    
    utilisateurs_non_amis = User.objects.exclude(
        id__in=request.user.amis.all().values_list('id', flat=True)
    ).exclude(id=request.user.id)

    if request.method == 'POST':
        action = request.POST.get('action')
        ami_id = request.POST.get('ami_id')
        
        # Vérifier si l'ami_id est vide
        if not ami_id and action == 'ajouter':
            messages.error(request, "Veuillez sélectionner un utilisateur.")
            return redirect('users:profile')
        
        try:
            ami = User.objects.get(id=ami_id)
            
            if action == 'ajouter':
                request.user.amis.add(ami)
                messages.success(request, f"{ami.first_name} {ami.last_name} a été ajouté à vos relations.")
            
            elif action == 'supprimer':
                request.user.amis.remove(ami)
                messages.success(request, f"{ami.first_name} {ami.last_name} a été retiré de vos relations.")
                
            return redirect('users:profile')
            
        except User.DoesNotExist:
            messages.error(request, "L'utilisateur sélectionné n'existe pas.")
    
    context = {
        'utilisateurs_non_amis': utilisateurs_non_amis
    }
    
    return render(request, 'users/profile.html', context)

def index_view(request):
    if request.user.is_authenticated:
        return redirect('ressources:list')
    return render(request, 'index.html')

def info(request):
    return render(request, 'info.html')