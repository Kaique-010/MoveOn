from email import message
from django.db.models.signals import post_save
from django.db.models.signals import post_migrate
from django.db import migrations
from django.dispatch import receiver
import requests
from .models import SLA, Category, Role, SLAPriority, Team, TicketAlert, Ticket, TicketStatus

@receiver(post_save, sender=Ticket)
def send_alert(sender, instance, **kwargs):
    if instance.status and instance.status.name in ["Resolvido", "Cancelado", "Fechado"]:
        alert = TicketAlert.objects.create(
            ticket=instance,
            message=f"Ticket #{instance.id} foi atualizado para {instance.status.name}"
        )

        if alert.webhook_url:
            try:
                requests.post(alert.webhook_url, json={"message": alert.message})
            except Exception as e:
                print(f"Erro ao Enviar webhook: {e}") 



@receiver(post_migrate)
def load_default_data(sender, **kwargs):
    print(f"Rodando post_migrate para: {sender.name}")
    if sender.name != "move_on":
        return  

    if not SLA.objects.exists():
        SLA.objects.bulk_create([
            SLA(priority=SLAPriority.LOW, response_time=4, resolution_time=10),
            SLA(priority=SLAPriority.MEDIUM, response_time=2, resolution_time=5),
            SLA(priority=SLAPriority.HIGH, response_time=2, resolution_time=2),
            SLA(priority=SLAPriority.CRITICAL, response_time=1, resolution_time=1),
        ])
        print("Criados os SLAs")

    if not Role.objects.exists():
        Role.objects.bulk_create([
            Role(name='Admin', description='Administrador do sistema'),
            Role(name='Analista', description='Analista de Chamados'),
            Role(name='Técnico', description='Responsável pela resolução de chamados'),
            Role(name='Desenvolvedor', description='Desenvolvedor'),
        ])
        print("Criados os Roles para usuarios padrão")

    if not TicketStatus.objects.exists():
        TicketStatus.objects.bulk_create([
            TicketStatus(name='Aberto', color='blue'),
            TicketStatus(name='Em Análise', color='yellow'),
            TicketStatus(name='Em Andamento', color='orange'),
            TicketStatus(name='Resolvido', color='green'),
            TicketStatus(name='Fechado', color='gray'),
        ])
        print("Criados os Status dos Tkts")

    if not Team.objects.exists():
        Team.objects.create(name="Admins"),
        Team.objects.create(name="Desenvolvedores"),
        Team.objects.create(name="Clientes"),
        Team.objects.create(name="Técnicos"),
        print("Criados os Times")
    
    if not Category.objects.exists():
        Category.objects.create(name="Chat"),
        Category.objects.create(name="Corretivas"),
        Category.objects.create(name="Atendimentos normais"),
        Category.objects.create(name="Atendimentos Emergenciais"),
        Category.objects.create(name="Melhorias"),
        print("Criadas as Categorias")


class Migration(migrations.Migration):

    dependencies = [
        
    ]

    operations = [
        migrations.RunPython(load_default_data),

    ]