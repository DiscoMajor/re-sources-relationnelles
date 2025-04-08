# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Citoyen

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember-me') == 'on'
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            
            if not remember_me:
                request.session.set_expiry(0)
                
            messages.success(request, f"Connexion réussie ! Bienvenue {user.prenom} {user.nom}")
            return redirect('index')
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    
    return render(request, 'users/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
        
    if request.method == 'POST':
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')
        
        if password != password_confirmation:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'users/register.html')
        
        # Vérification si l'email existe déjà
        if Citoyen.objects.filter(email=email).exists():
            messages.error(request, "Un compte avec cet email existe déjà.")
            return render(request, 'users/register.html')
        
        # Création du nouvel utilisateur
        user = Citoyen(
            prenom=prenom,
            nom=nom,
            email=email
        )
        user.set_password(password)  # Utilise notre méthode pour hacher le mot de passe
        user.save()
        
        # Authentification et connexion
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            
        messages.success(request, f"Compte créé avec succès ! Bienvenue {prenom} {nom}")
        return redirect('index')
        
    return render(request, 'users/register.html')

def logout_view(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('index')

@login_required
def profile_view(request):
    return render(request, 'users/profile.html')