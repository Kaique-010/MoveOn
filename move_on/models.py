from datetime import timedelta, timezone
from tkinter.tix import Tree
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import timedelta


#1- Modelo para todos os Clientes e perfis 
class Profile(models.Model):
    name = models.CharField("Nome da Empresa", max_length=150)
    document = models.CharField("CPF/CNPJ", max_length=18, unique=True)
    email = models.EmailField("E-mail", unique=True)
    phone = models.CharField("Telefone", max_length=20, blank=True, null=True)
    active = models.BooleanField("Ativo?", default=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)

    class Meta:
        db_table = "profiles"

    def __str__(self):
        return f"{self.name} - {'Ativo' if self.active else 'Inativo'}"

    def save(self, *args, **kwargs):
        self.name = self.name.upper().strip()
        super().save(*args, **kwargs)


# 2. Modelo de Roles (Permite Adição de Novos Papéis)
class Role(models.Model):
    name = models.CharField("Nome do Papel", max_length=50, unique=True)
    description = models.TextField("Descrição", blank=True, null=True)

    class Meta:
        db_table = "roles"

    def __str__(self):
        return self.name




# 3. Modelo User 
class User(AbstractUser):
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="users", null=True, blank=True, db_column='client')
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, db_column='role')

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
        return f"{self.username} ({self.role})" if self.role else self.username




#4- modelo dePrioridades dos Tkts segue sendo um choices
class SLAPriority(models.TextChoices):
    LOW = "low", "Low"
    MEDIUM = "medium", "Medium"
    HIGH = "high", "High"
    CRITICAL = "critical", "Critical"

    @classmethod
    def get_color(cls, value):
        color_map = {
            cls.LOW: '#00c16c',  
            cls.MEDIUM: '#ffc52c', 
            cls.HIGH: '#ff9915', 
            cls.CRITICAL: '#CC3733',  
        }
        return color_map.get(value, 'gray')


#5- Modelo das SLA 
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


#6-Status dos Tkts
class TicketStatus(models.Model):
    name = models.CharField("Status", max_length=50, unique=True)

    class Meta:
        db_table = "ticket_status"

    def __str__(self):
        return self.name


class Team(models.Model):
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="teams", blank=True, null=True)
    name = models.CharField("Nome da Equipe", max_length=150)
    roles = models.ManyToManyField(Role, related_name="teams", blank=True)  
    members = models.ManyToManyField(User, related_name="teams", blank=True)  

    class Meta:
        db_table = "teams"

    def __str__(self):
        return f"{self.name}"
    
    
class Category(models.Model):
    name = models.CharField("Nome", max_length=100)
    description = models.TextField("Descrição", blank=True, null=True)

    class Meta:
        db_table = "categorias"

    def __str__(self):
        return self.name


class Ticket(models.Model):
    client = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="tickets", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tickets", null=True, blank=True)
    assigned_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name="tickets")
    sla = models.ForeignKey(SLA, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField("Título", max_length=255, null=True, blank=True)
    description = models.TextField("Descrição", null=True, blank=True)
    status = models.ForeignKey(TicketStatus, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizado em", auto_now=True)
    due_date = models.DateTimeField("Previsão", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    log = models.TextField("Log de Alterações", blank=True)

    class Meta:
        db_table = "tickets"

    def __str__(self):
        return f"#{self.id} - {self.title} ({self.status})"

    def can_transition(self, user, to_status):
        if not self.status:
            return False  

        transition = WorkflowTransition.objects.filter(
            workflow__client=self.client,
            from_status=self.status,
            to_status=to_status,
            allowed_roles__in=[user.role]
        ).exists()

        return transition

    def change_status(self, user, to_status):
        if not self.can_transition(user, to_status):
            raise PermissionError("Você não tem permissão para essa transição.")

        old_status = self.status
        self.status = to_status
        self.save()

        self.log += f"\n[{timezone.now()}] {user.username} alterou status de {old_status} para {to_status}"
        self.save()

    def save(self, *args, **kwargs):
        if not self.due_date and self.sla:
            sla_time = self.sla.get_resolution_time()  
            if sla_time:
                self.due_date = timezone.now() + sla_time  

        super().save(*args, **kwargs)


class TicketAction(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="actions")
    action_number = models.IntegerField("Número da Ação")
    performed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField("Descrição da Ação")
    assigned_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True)
    action_date = models.DateTimeField("Data da Ação", default=timezone.now)
    action_start_time = models.TimeField("Hora de Início", null=True, blank=True)
    action_end_time = models.TimeField("Hora de Fim", null=True, blank=True)
    audio = models.FileField(upload_to="tickets/audios/", null=True, blank=True)
    image = models.ImageField(upload_to="tickets/images/", null=True, blank=True)

    class Meta:
        db_table = "ticket_actions"
        ordering = ["action_number"]

    def __str__(self):
        return f"Ação {self.action_number} no Ticket #{self.ticket.id} por {self.performed_by.username}"

    @classmethod
    def register_action(cls, ticket, user, description, assigned_team=None, start_time=None, end_time=None, audio=None, image=None):
        """ Registra uma nova ação no ticket """
        last_action = cls.objects.filter(ticket=ticket).order_by("-action_number").first()
        action_number = last_action.action_number + 1 if last_action else 1

        action = cls.objects.create(
            ticket=ticket,
            action_number=action_number,
            performed_by=user,
            description=description,
            assigned_team=assigned_team,
            action_start_time=start_time,
            action_end_time=end_time,
            audio=audio,
            image=image
        )

        # Atualiza o log do ticket
        ticket.log += f"\n[{timezone.now()}] Ação {action_number} realizada por {user.username}: {description}"
        ticket.save()

        return action


class Workflow(models.Model):
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="workflows")
    name = models.CharField("Nome do Workflow", max_length=255)
    description = models.TextField("Descrição do Workflow", blank=True, null=True)
    initial_status = models.ForeignKey(TicketStatus, on_delete=models.SET_NULL, null=True, related_name="initial_workflows")
    final_status = models.ForeignKey(TicketStatus, on_delete=models.SET_NULL, null=True, related_name="final_workflows")

    def __str__(self):
        return self.name


class WorkflowTransition(models.Model):
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, related_name="transitions")
    from_status = models.ForeignKey(TicketStatus, on_delete=models.CASCADE, related_name="from_transitions")
    to_status = models.ForeignKey(TicketStatus, on_delete=models.CASCADE, related_name="to_transitions")
    allowed_roles = models.ManyToManyField(Role, related_name="allowed_transitions")  # Roles que podem realizar essa transição
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('workflow', 'from_status', 'to_status')

    def __str__(self):
        return f"{self.from_status.name} -> {self.to_status.name}"






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


