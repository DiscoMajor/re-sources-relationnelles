from django.db import models

class Comment(models.Model):
    citoyen = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='comments')
    ressource = models.ForeignKey('ressources.Ressource', on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.citoyen} ({self.created_at.strftime('%d/%m/%Y %H:%M')})"