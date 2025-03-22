from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now


class Client(models.Model):
    name = models.CharField("Nome da Empresa", max_length=150)
    document = models.CharField("CPF/CNPJ", max_length=18, unique=True)
    email = models.EmailField("E-mail", unique=True)
    phone = models.CharField("Telefone", max_length=20, blank=True, null=True)
    active = models.BooleanField("Ativo?", default=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        db_table = "clients"

    def __str__(self):
        return f"{self.name} - {'Ativo' if self.active else 'Inativo'}"

    def save(self, *args, **kwargs):
        self.name = self.name.upper().strip()
        super().save(*args, **kwargs)


class RoleChoices(models.TextChoices):
    ADMIN = "admin", "Administrator"
    ANALYST = "analyst", "Analyst"
    TECHNICIAN = "technician", "Technician"
    DEVELOPER = "developer", "Developer"
    CUSTOMER = "customer", "Customer"


class User(AbstractUser):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="users", null=True, blank=True)
    role = models.CharField(max_length=30, choices=RoleChoices.choices)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='move_on_users',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='move_on_users',
        blank=True
    )

    class Meta:
        db_table = "users"

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class SLAPriority(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    CRITICAL = "critical", "Critical"

    @classmethod
    def get_color(cls, value):
        color_map = {
            cls.LOW: 'green',  # Verde para baixa prioridade
            cls.MEDIUM: 'yellow',  # Amarelo para média prioridade
            cls.HIGH: 'black',  # Laranja para alta prioridade
            cls.CRITICAL: 'red',  # Vermelho para prioridade crítica
        }
        return color_map.get(value, 'gray')


class SLA(models.Model):
    priority = models.CharField("Prioridade",max_length=10, choices=SLAPriority.choices)
    response_time = models.IntegerField("Tempo de Resposta (dias)")
    resolution_time = models.IntegerField("Tempo de Resolução (dias)")

    def get_response_time(self):
        return timedelta(days=self.response_time)

    def get_resolution_time(self):
        return timedelta(days=self.resolution_time)

    def __str__(self):
        return f"{self.get_priority_display()} - {self.resolution_time} dias"

    class Meta:
        db_table = "sla"



class TicketStatus(models.TextChoices):
    NEW = "new", "New"
    UNDER_ANALYSIS = "under_analysis", "Under Analysis"
    IN_DEVELOPMENT = "in_development", "In Development"
    WAITING_CUSTOMER = "waiting_customer", "Waiting for Customer"
    RESOLVED = "resolved", "Resolved"
    CANCELED = "canceled", "Canceled"
    CLOSED = "closed", "Closed"


class Ticket(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name="tickets")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tickets")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets")
    sla = models.ForeignKey(SLA, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField("Título", max_length=255)
    description = models.TextField("Descrição")
    status = models.CharField("Status", max_length=20, choices=TicketStatus.choices, default=TicketStatus.NEW)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "tickets"

    def __str__(self):
        return f"#{self.id} - {self.title} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        self.title = self.title.upper().strip()
        if not self.due_date and self.sla:
            self.due_date = now() + self.sla.resolution_time
        super().save(*args, **kwargs)

    def is_late(self):
        return bool(self.due_date and now() > self.due_date)


class TicketAlert(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="alerts")
    message = models.TextField("Mensagem")
    sent_at = models.DateTimeField(auto_now_add=True)
    webhook_url = models.URLField("Webhook", blank=True, null=True)
    api_endpoint = models.URLField("API Endpoint", blank=True, null=True)

    class Meta:
        db_table = "alerts"

    def __str__(self):
        return f"Alert for Ticket #{self.ticket.id} at {self.sent_at}"

    def save(self, *args, **kwargs):
        self.message = self.message.strip()
        super().save(*args, **kwargs)
