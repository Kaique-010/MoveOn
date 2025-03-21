from django.contrib import admin
from .models import Client, User, SLA, Ticket, TicketAlert

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'document', 'email', 'active', 'created_at')
    search_fields = ('name', 'document', 'email')
    list_filter = ('active',)
    ordering = ('-created_at',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'client', 'email')
    search_fields = ('username', 'email')
    list_filter = ('role', 'client')


@admin.register(SLA)
class SLAAdmin(admin.ModelAdmin):
    list_display = ('priority', 'response_time', 'resolution_time')
    search_fields = ('priority',)
    list_filter = ('priority',)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'client', 'created_by', 'assigned_to', 'created_at', 'due_date')
    search_fields = ('title', 'description')
    list_filter = ('status', 'client', 'created_by', 'assigned_to')
    ordering = ('-created_at',)


@admin.register(TicketAlert)
class TicketAlertAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'message', 'sent_at', 'webhook_url', 'api_endpoint')
    search_fields = ('message', 'ticket__id')
    list_filter = ('sent_at',)
