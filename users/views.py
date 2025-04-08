from django.shortcuts import render, redirect
from django.contrib import messages

def login_view(request):
    """
    Vue pour afficher le template de connexion et gérer la soumission du formulaire.
    Pour l'instant, simule simplement une connexion réussie sans authentification réelle.
    """
    if request.method == 'POST':
        # Récupérer les données du formulaire
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Pour l'instant, on simule juste une connexion réussie
        # Plus tard, on implémentera l'authentification réelle
        messages.success(request, f"Connexion réussie avec l'email {email}")
        return redirect('index') 
        
    return render(request, 'users/login.html')

def register_view(request):
    """
    Vue pour afficher le template d'inscription et gérer la soumission du formulaire.
    Pour l'instant, simule simplement une création de compte réussie.
    """
    if request.method == 'POST':
        # Récupérer les données du formulaire
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        
        # Pour l'instant, on simule juste la création de compte
        # Plus tard, on implémentera la création réelle d'utilisateur
        messages.success(request, f"Félicitations {prenom} {nom} ! Votre compte a été créé avec succès.")
        return redirect('index')
        
    return render(request, 'users/register.html')