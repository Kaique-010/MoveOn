from django.db import models
from django.contrib.auth.models import User

from core import settings

class ChatRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chatrooms'
    
    def __str__(self):
        return self.name

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
    
    def __str__(self):
        return f"{self.user.username if self.user else 'Anônimo'}: {self.text[:30]}"
    

class ChatTicket(models.Model):
    room = models.OneToOneField(ChatRoom, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    
    
    class Meta:
        db_table = 'chat_tkts'

    def __str__(self):
        return f"Ticket #{self.id} - {'Resolvido' if self.resolved else 'Pendente'}"
