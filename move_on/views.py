from encodings.punycode import T
from pyexpat import model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.views.generic import TemplateView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse_lazy
from .models import SLA, Category, Team, Ticket, TicketAction, TicketAlert, TicketStatus, User
from .forms import CategoryForm, SLAForm, TeamForm, TicketAlertForm, TicketFilterForm, TicketForm, TicketStatusForm, UserForm, UserUpdateForm
from django.db.models import Q

class MenuViewiew(LoginRequiredMixin,TemplateView):
    template_name = 'Menu/menu.html'

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'

    def get_queryset(self):
        user = self.request.user
        self.form = TicketFilterForm(self.request.GET)

        # Define o queryset inicial baseado no usuário
        if user.is_superuser:
            queryset = Ticket.objects.all()
        else:
            queryset = Ticket.objects.filter(
                Q(client=user.client) & (Q(created_by=user) | Q(client=user.client))
            )

        # Aplica os filtros se o formulário for válido
        if self.form.is_valid():
            if self.form.cleaned_data["title"]:
                queryset = queryset.filter(title__icontains=self.form.cleaned_data["title"])
            if self.form.cleaned_data["status"]:
                queryset = queryset.filter(status=self.form.cleaned_data["status"])
            if self.form.cleaned_data["assigned_team"]:
                queryset = queryset.filter(assigned_team=self.form.cleaned_data["assigned_team"])
            if self.form.cleaned_data["sla"]:
                queryset = queryset.filter(sla=self.form.cleaned_data["sla"])
            if self.form.cleaned_data["category"]:
                queryset = queryset.filter(category=self.form.cleaned_data["category"])
            if self.form.cleaned_data["created_at_start"]:
                queryset = queryset.filter(created_at__date__gte=self.form.cleaned_data["created_at_start"])
            if self.form.cleaned_data["created_at_end"]:
                queryset = queryset.filter(created_at__date__lte=self.form.cleaned_data["created_at_end"])
            if self.form.cleaned_data["client"]:
                queryset = queryset.filter(client__name__icontains=self.form.cleaned_data["client"])

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = self.form
        return context

class TicketDetailView(LoginRequiredMixin, DetailView):
        model = Ticket
        template_name = "tickets/ticket_detail.html"
        context_object_name = "ticket"

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["actions"] = self.get_ticket_actions()
            return context

        def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["actions"] = self.object.actions.all()  # Pegando todas as ações do ticket
            return context


# views.py

class TicketCreate(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'tickets/tickets_form.html'
    success_url = 'list'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.client = self.request.user.client
        ticket = form.save()

        # Obtém dados do TicketAction
        action_description = form.cleaned_data.get('action_description')
        action_start_time = form.cleaned_data.get('action_start_time')
        action_end_time = form.cleaned_data.get('action_end_time')

        # Registra a ação no ticket
        TicketAction.register_action(
            ticket=ticket,
            user=self.request.user,
            description=action_description,
            assigned_team=form.cleaned_data.get("assigned_team"),
            start_time=action_start_time,
            end_time=action_end_time
        )
        
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

    def form_valid(self, form):
        # Salva o ticket
        ticket = form.save()

        # Obtém dados do TicketAction
        action_description = form.cleaned_data.get('action_description')
        action_start_time = form.cleaned_data.get('action_start_time')
        action_end_time = form.cleaned_data.get('action_end_time')

        # Registra a ação no ticket
        TicketAction.register_action(
            ticket=ticket,
            user=self.request.user,
            description=action_description,
            assigned_team=form.cleaned_data.get("assigned_team"),
            start_time=action_start_time,
            end_time=action_end_time
        )

        return super().form_valid(form)

    


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



class ParamsView(LoginRequiredMixin,TemplateView):
    template_name = 'Param/params.html'

class SLACreateView(LoginRequiredMixin, CreateView):
    model = SLA
    form_class = SLAForm
    template_name = 'SLA/sla_form.html'
    success_url = reverse_lazy('sla_list') 

    def form_valid(self, form):

        return super().form_valid(form)


class SlaList(LoginRequiredMixin, ListView):
    model = SLA
    template_name = 'SLA/sla_list.html'
    context_object_name = 'slas'
    
    def get_queryset(self):
        
        user= self.request.user
        
        if user.is_superuser:
            return SLA.objects.all()

class SlaUpdateView(LoginRequiredMixin, UpdateView):
    model = SLA
    template_name = 'SLA/sla_form.html'
    form_class = SLAForm
    context_object_name = 'slas'
    success_url = reverse_lazy('sla_list')
    
    def get_queryset(self):
        return super().get_queryset()
    
    
    
class SlaDeleteView(LoginRequiredMixin, DeleteView):
    model = SLA
    template_name = 'SLA/sla_delete.html'
    success_url = reverse_lazy('sla_list')
    
    
class CategoryList(LoginRequiredMixin, ListView):
    model=Category
    template_name= 'Category/categories_list.html'
    context_object_name = 'categories'

class CategoryCreate(LoginRequiredMixin, CreateView):
    model=Category
    template_name= 'Category/category_form.html'
    form_class = CategoryForm
    success_url = reverse_lazy('categories_list')
    
    def form_valid(self, form):
        return super().form_valid(form)

class CategoriesUpdate(LoginRequiredMixin, UpdateView):
    model=Category
    form_class = CategoryForm
    template_name= 'Category/category_form.html'
    success_url = reverse_lazy('categories_list')
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class CategoriesDelete(LoginRequiredMixin, DeleteView):
    model=Category
    template_name= 'Category/category_delete.html'
    success_url = reverse_lazy('categories_list')
    

class StatusTicketListView(LoginRequiredMixin, ListView):
    model=TicketStatus
    template_name = 'Status/status_list.html'
    context_object_name = 'status'

class StatusTicketCreateView(LoginRequiredMixin, CreateView):
    model=TicketStatus
    template_name= 'Status/status_form.html'
    form_class= TicketStatusForm
    success_url = reverse_lazy('status_list')
    
    def form_invalid(self, form):
        return super().form_invalid(form)

class StatusTicketUpdateView(LoginRequiredMixin, UpdateView):
    model=TicketStatus
    template_name='Status/status_form.html'
    form_class=TicketStatusForm
    success_url= reverse_lazy('status_list')
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class StatusTicketDeleteView(LoginRequiredMixin, DeleteView):
    model=TicketStatus
    template_name= 'Status/status_delete.html'
    success_url= reverse_lazy('status_list')
    
    def get_object(self, queryset=None):
        print("PK recebido:", self.kwargs.get("pk")) 
        return super().get_object(queryset)



   
class TeamList(LoginRequiredMixin, ListView):
    model=Team
    template_name= 'Team/team_list.html'
    context_object_name = 'teams'
    
    def get_queryset(self):
        return Team.objects.prefetch_related('roles', 'members').all()

class TeamCreateView(LoginRequiredMixin, CreateView):
    model=Team
    template_name= 'Team/team_form.html'
    form_class = TeamForm
    success_url = reverse_lazy('team_list')
    
    def form_valid(self, form):
        return super().form_valid(form)

class TeamUpdateView(LoginRequiredMixin, UpdateView):
    model=Team
    form_class = TeamForm
    template_name= 'Team/team_form.html'
    success_url = reverse_lazy('team_list')
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class TeamDeleteView(LoginRequiredMixin, DeleteView):
    model=Team
    template_name= 'Team/team_delete.html'
    success_url = reverse_lazy('team_list')
    

# 🔹 Listar usuários
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = "User/user_list.html"
    context_object_name = "users"

# 🔹 Criar usuário
class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = "User/user_form.html"
    success_url = reverse_lazy("user_list")

# 🔹 Atualizar usuário
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = "User/user_form.html"
    success_url = reverse_lazy("user_list")

# 🔹 Deletar usuário
class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = "User/user_delete.html"
    success_url = reverse_lazy("user_list")