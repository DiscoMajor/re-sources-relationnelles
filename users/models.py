from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class AbstractUser(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_authenticated = True
    is_anonymous = False
    
    class Meta:
        abstract = True
        
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

class Citoyen(AbstractUser):
    citycode = models.CharField(max_length=7)
    amis = models.ManyToManyField('self', symmetrical=True)
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"
    

class Moderator(AbstractUser):
    is_active_moderator = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    

class Admin(AbstractUser):
    is_active_admin = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    

class SuperAdmin(AbstractUser):
    is_active_superadmin = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.prenom} {self.nom}"