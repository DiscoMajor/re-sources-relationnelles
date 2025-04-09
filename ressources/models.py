from django.db import models

class Type(models.Model):
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label

class Ressource(models.Model):
    title = models.CharField(max_length=500)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    author = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='created_resources')
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    def is_visible_to(self, user):
        if not self.is_private:
            return True
        if self.author == user:
            return True
        if hasattr(user, 'amis') and self.author in user.amis.all():
            return True
        return False
        
    