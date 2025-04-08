from django.contrib.auth.backends import BaseBackend
from .models import Citoyen, Moderator, Admin, SuperAdmin

class EmailBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # username contient l'email dans notre cas
        user = None
        
        # Vérifie chaque type d'utilisateur
        for model in [Citoyen, Moderator, Admin, SuperAdmin]:
            try:
                user = model.objects.get(email=username)
                
                # Vérifie le mot de passe
                if user.check_password(password):
                    return user
                return None  # Mot de passe incorrect
                
            except model.DoesNotExist:
                continue
        
        return None  # Aucun utilisateur trouvé
    
    def get_user(self, user_id):
        for model in [Citoyen, Moderator, Admin, SuperAdmin]:
            try:
                return model.objects.get(pk=user_id)
            except model.DoesNotExist:
                continue
        return None