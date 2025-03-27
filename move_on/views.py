from encodings.punycode import T
from pyexpat import model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.views.generic import TemplateView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse_lazy
from .models import SLA, Ticket, TicketAlert, TicketStatus
from .forms import SLAForm, TicketForm
from django.db.models import Q

class MenuViewiew(LoginRequiredMixin,TemplateView):
    template_name = 'Menu/menu.html'

class TicketListView(LoginRequiredMixin,ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'
    
def get_queryset(self):
        
        user= self.request.user
        
        if user.is_superuser:
            return Ticket.objects.all()
        return Ticket.objects.filter(
            Q(client=user.client) &
            (Q(createted_by=user)) | Q(assigned_by=user) | Q(client=user.client)
        )


class TicketDetail(LoginRequiredMixin, DetailView):
    model = Ticket
    template_name = 'tickets/tickets_detail'
    
    def get_queryset(self):
        user = self.request.user
        return Ticket.objects.filter(client=user.client)



class TicketCreate(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/tickets_form.html'
    success_url = 'list'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.client = self.request.user.client
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)  # Para depuração no terminal
        return self.render_to_response(self.get_context_data(form=form))
    

class TicketUpdate(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/tickets_form.html'
    success_url = reverse_lazy("ticket_list")

    def get_queryset(self):
        return Ticket.objects.all()
    


class TicketDelete(LoginRequiredMixin, DeleteView):
    model = Ticket
    form_class = TicketForm
    template_name = "tickets/ticket_delete.html"
    success_url = reverse_lazy("ticket_list")
    

    def delete(self, request, *args, **kwargs):
        ticket = self.get_object()
        print(f"Excluindo o ticket: {ticket.id}")  
        response = super().delete(request, *args, **kwargs)
        return response


    

class SLACreateView(LoginRequiredMixin, CreateView):
    model = SLA
    form_class = SLAForm
    template_name = 'tickets/sla_create.html'
    success_url = reverse_lazy('sla_list') 

    def form_valid(self, form):

        return super().form_valid(form)


class SlaList(LoginRequiredMixin, ListView):
    model = SLA
    template_name = 'tickets/sla_list.html'
    context_object_name = 'sla'
    
    def get_queryset(self):
        
        user= self.request.user
        
        if user.is_superuser:
            return SLA.objects.all()
        
