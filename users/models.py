from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    citycode = models.CharField(max_length=7, blank=True, null=True)
    is_active_moderator = models.BooleanField(default=False)
    is_active_admin = models.BooleanField(default=False)
    is_active_superadmin = models.BooleanField(default=False)
    amis = models.ManyToManyField('self', symmetrical=True, blank=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name and self.last_name else self.username