from django.db import models
from django.utils import timezone

class Room(models.Model):
    name = models.CharField(max_length=500)
    is_group = models.BooleanField(default=False)
    participants = models.ManyToManyField('users.User', related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class Message(models.Model):
    value = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='created_messages')
    room = models.ForeignKey('chat.Room', on_delete=models.CASCADE, related_name='messages')
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user}: {self.value[:50]}..."
    
    class Meta:
        ordering = ['create_at']
        