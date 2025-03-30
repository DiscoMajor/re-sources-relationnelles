from django.db import models

class Type(models.Model):
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label

class Ressource(models.Model):
    title = models.CharField(max_length=500)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    relation = models.ManyToManyField('users.Citoyen')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title