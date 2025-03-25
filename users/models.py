from django.db import models

class AbstractUser(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return
    

class Citoyen(AbstractUser):
    citycode = models.CharField(max_length=7)

    def __str__(self):
        return
    

class Moderator(AbstractUser):
    is_active_moderator = models.BooleanField(default=True)

    def __str__(self):
        return
    

class Admin(AbstractUser):
    is_active_admin = models.BooleanField(default=True)

    def __str__(self):
        return
    

class SuperAdmin(AbstractUser):
    is_active_superadmin = models.BooleanField(default=True)

    def __str__(self):
        return