from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import timedelta, timezone


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

class User(AbstractUser):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="users")
    role = models.CharField(max_length=30, choices=RoleChoices.choices)
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='move_on_users',  # Altere o related_name para algo único
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', 
        related_name='move_on_users',  # Altere o related_name para algo único
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


class SLA(models.Model):
    priority = models.CharField(max_length=50)
    response_time = models.DurationField()
    resolution_time = models.DurationField()
    
    def __str__(self):
        return f"{self.priority} - {self.resolution_time}"
    


class TicketStatus(models.TextChoices):
    NEW = "new", "New"
    UNDER_ANALYSIS = "under_analysis", "Under Analysis"
    IN_DEVELOPMENT = "in_development", "In Development"
    WAITING_CUSTOMER = "waiting_customer", "Waiting for Customer"
    RESOLVED = "resolved", "Resolved"
    CANCELED = "canceled", "Canceled"
    CLOSED = "closed", "Closed"

class Ticket(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="tickets")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tickets")
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets")
    sla = models.ForeignKey(SLA, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField("Título", max_length=255)
    description = models.TextField("Descrição")
    status = models.CharField(max_length=20, choices=TicketStatus.choices, default=TicketStatus.NEW)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "tickets"

    def __str__(self):
        return f"#{self.id} - {self.title} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        self.title = self.title.upper().strip()
        self.description = self.description.upper().strip()
        super().save(*args, **kwargs)

    def is_late(self):
        return self.due_date and self.due_date < timezone.now()


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
        self.message = self.message.upper().strip()
        super().save(*args, **kwargs)




