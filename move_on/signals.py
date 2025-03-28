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
def load_default_data(sender, using, **kwargs):  # <-- Recebe o `using`
    print(f"Rodando post_migrate para: {sender.name}")
    if sender.name != "move_on":
        return  

    if not SLA.objects.using(using).exists():  # <-- Usa o banco correto
        SLA.objects.using(using).bulk_create([
            SLA(priority=SLAPriority.LOW, response_time=4, resolution_time=10),
            SLA(priority=SLAPriority.MEDIUM, response_time=2, resolution_time=5),
            SLA(priority=SLAPriority.HIGH, response_time=2, resolution_time=2),
            SLA(priority=SLAPriority.CRITICAL, response_time=1, resolution_time=1),
        ])
        print("Criados os SLAs")

    if not Role.objects.using(using).exists():
        Role.objects.using(using).bulk_create([
            Role(name='Admin', description='Administrador do sistema'),
            Role(name='Analista', description='Analista de Chamados'),
            Role(name='Técnico', description='Responsável pela resolução de chamados'),
            Role(name='Desenvolvedor', description='Desenvolvedor'),
        ])
        print("Criados os Roles para usuários padrão")

    if not TicketStatus.objects.using(using).exists():
        TicketStatus.objects.using(using).bulk_create([
            TicketStatus(name='Aberto'),
            TicketStatus(name='Em Análise'),
            TicketStatus(name='Em Andamento'),
            TicketStatus(name='Resolvido'),
            TicketStatus(name='Fechado'),
        ])
        print("Criados os Status dos Tkts")

    if not Team.objects.using(using).exists():
        Team.objects.using(using).bulk_create([
            Team(name="Admins"),
            Team(name="Desenvolvedores"),
            Team(name="Clientes"),
            Team(name="Técnicos"),
        ])
        print("Criados os Times")

    if not Category.objects.using(using).exists():
        Category.objects.using(using).bulk_create([
            Category(name="Chat"),
            Category(name="Corretivas"),
            Category(name="Atendimentos normais"),
            Category(name="Atendimentos Emergenciais"),
            Category(name="Melhorias"),
        ])
        print("Criadas as Categorias")
