from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.conf import settings


# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError(_('The email must be set'))
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save()
#         return user

#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError(_('Superuser must have is_staff=True.'))
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError(_('Superuser must have is_superuser=True.'))
#         return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    userfirstname = models.CharField('Nom', max_length=255, blank=False, null=False)
    usersurname = models.CharField('Prénom', max_length=255, blank=False, null=False)
    email = models.EmailField('Courriel', unique=True)
    is_doi = models.BooleanField(default=False)
    doi_at = models.DateTimeField("Date DOI", null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_identity(self):
        return "%s %s" % (self.first_name, self.last_name)


class ConnectionLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=255, null=True, blank=True)