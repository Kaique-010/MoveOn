from email import message
from django.db.models.signals import post_save
from django.dispatch import receiver
import requests
from .models import TicketAlert, Ticket

@receiver(post_save, sender=Ticket)
def send_alert(sender, instance, **kwargs):
    if instance.status in ["resolved", "canceled", "closed"]:
        alert = TicketAlert.objects.create(
            ticket=instance,
            message=f"Ticket #{instance.id} foi atualizado para  {instance.get_status_display()}"
        )
        
        if alert.webhook_url:
            try:
                requests.post(alert.webhook_url, json={"message": alert.message})
            except Exception as e:
                print(f"Erro ao Enviar webhook: {e}")