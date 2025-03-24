from django.contrib import admin
from .models import Profile, Role, User, SLA, TicketStatus, Team, Ticket, Workflow, WorkflowTransition, TicketAlert

# Admin para o modelo Profile
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'document', 'email', 'phone', 'active', 'created_at')
    search_fields = ('name', 'document', 'email')
    list_filter = ('active',)

# Admin para o modelo Role
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# Admin para o modelo User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'client', 'role', 'email', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'client__name')
    list_filter = ('is_active', 'role', 'client')

# Admin para o modelo SLA
@admin.register(SLA)
class SLAAdmin(admin.ModelAdmin):
    list_display = ('priority', 'response_time', 'resolution_time')
    list_filter = ('priority',)

# Admin para o modelo TicketStatus
@admin.register(TicketStatus)
class TicketStatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Admin para o modelo Team
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'client')
    search_fields = ('name', 'client__name')
    filter_horizontal = ('roles', 'members')

# Admin para o modelo Ticket
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'status', 'created_by', 'assigned_team', 'created_at', 'updated_at', 'due_date')
    search_fields = ('title', 'created_by__username', 'assigned_team__name', 'status__name')
    list_filter = ('status', 'assigned_team', 'client')
    raw_id_fields = ('created_by', 'assigned_team', 'sla', 'status')

# Admin para o modelo Workflow
@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'initial_status', 'final_status')
    search_fields = ('name', 'client__name')

# Admin para o modelo WorkflowTransition
@admin.register(WorkflowTransition)
class WorkflowTransitionAdmin(admin.ModelAdmin):
    list_display = ('workflow', 'from_status', 'to_status', 'is_active')
    list_filter = ('is_active', 'workflow', 'from_status', 'to_status')
    filter_horizontal = ('allowed_roles',)

# Admin para o modelo TicketAlert
@admin.register(TicketAlert)
class TicketAlertAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'message', 'sent_at', 'webhook_url', 'api_endpoint')
    search_fields = ('ticket__id', 'message')
    list_filter = ('sent_at',)

