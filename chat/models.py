from django.db import models
from django.contrib.auth.models import User
from move_on.models import Profile, Team, Ticket
from core import settings

class ChatRoom(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, db_column='ticket_id')
    created_at = models.DateTimeField(auto_now_add=True)
    last_message = models.TextField(blank=True, null=True)

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


class Attendant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='attendant_profile')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="attendants")
    available = models.BooleanField(default=True) 

    class Meta:
        db_table = "attendants"

    def __str__(self):
        return f"{self.user.username} ({'Disponível' if self.available else 'Ocupado'})"
    

class ChatQueue(models.Model):
    ticket = models.OneToOneField(Ticket, on_delete=models.CASCADE, related_name="chat_queue")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "chat_queue"

    def __str__(self):
        return f"Fila para Ticket #{self.ticket.id} - {self.ticket.client.name}"


class ChatSettings(models.Model):
    client = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="chat_settings")
    auto_assign = models.BooleanField(default=True)  # Distribuição automática ou manual
    balance_tickets = models.BooleanField(default=True)  # Equilibrar tickets por atendente
    max_tickets_per_attendant = models.IntegerField(default=5)  # Limite por atendente

    class Meta:
        db_table = "chat_settings"

    def __str__(self):
        return f"Configuração de Chat - {self.client.name}"
