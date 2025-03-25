from django.db import models
import requests
from move_on.models import Ticket, User



# models.py (adicione esses modelos)

class TicketMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="messages")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField("Mensagem")
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    read_by = models.ManyToManyField(User, related_name="read_messages", blank=True)

    class Meta:
        db_table = "ticket_messages"
        ordering = ['created_at']

    def __str__(self):
        return f"Mensagem #{self.id} no Ticket #{self.ticket.id}"

    def mark_as_read(self, user):
        """Marca a mensagem como lida por um usuário"""
        self.read_by.add(user)
        
    @property
    def is_read(self):
        """Verifica se a mensagem foi lida pelo usuário atual"""
        if 'request' in globals():
            return self.read_by.filter(id=requests.request.user.id).exists()
        return False


class UserConnection(models.Model):
    """Rastreia conexões WebSocket dos usuários"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=255)
    connected_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "user_connections"

    def __str__(self):
        return f"Conexão de {self.user.username}"