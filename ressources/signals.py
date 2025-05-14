from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import ConnectionLog

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """
    Enregistre chaque connexion utilisateur
    """
    if request:
        # Récupérer l'adresse IP
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        
        ConnectionLog.objects.create(
            user=user,
            ip_address=ip,
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )