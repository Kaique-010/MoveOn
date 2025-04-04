from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, JsonResponse
from django.views.generic import TemplateView
from move_on.models import Ticket, Category, User
from notification.models import Notifications
from work_schedule.models import WorkSchedule

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        print("Formulário enviado:", request.POST)

        if form.is_valid():
            user = form.get_user()
            print(f"Usuário {user.username} autenticado com sucesso!")
            login(request, user)
            return redirect('/')
        else:
            print("Formulário de login inválido!")
            print(form.errors)  # Exibe os erros do formulário no console
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


from django.utils.timezone import now, localdate
from django.db.models import Count
from datetime import timedelta

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = localdate()  # Data de hoje
        week_start = today - timedelta(days=today.weekday())  # Início da semana (segunda-feira)
        month_start = today.replace(day=1)  # Início do mês
        categories = Category.objects.annotate(ticket_count=Count("ticket"))
        uncategorized_tickets = Ticket.objects.filter(category__isnull=True).count()
        usuarios = User.objects.annotate(ticket_count= Count("created_tickets"))
        unknow_user = Ticket.objects.filter(created_by__isnull=True).count()
        notifications = Notifications.objects.all().order_by('-created_at')[:10]
        work_schedule = WorkSchedule.objects.all().order_by('-id')[:5]
        
        # Definindo os papéis (roles) para simplificação
        roles = {
            'admins': 1, 
            'devs': 2,
            'tec': 4,
            'analista': 5, 
            'vazio': None
        }
        
        # Contagem de tickets por role
        roles_tkts = {}
        for role_name, role_id in roles.items():
            roles_tkts[role_name] = Ticket.objects.filter(assigned_team_id=role_id).count()

        # Contagens de tickets de hoje, semana e mês
        context['tickets_today'] = Ticket.objects.filter(created_by=user, created_at__date=today).count()
        context['tickets_week'] = Ticket.objects.filter(created_by=user, created_at__date__gte=week_start).count()
        context['tickets_month'] = Ticket.objects.filter(created_by=user, created_at__date__gte=month_start).count()
        
        context.update({
            'tickets_today': Ticket.objects.filter(created_by=user, created_at__date=today).count(),
            'tickets_week': Ticket.objects.filter(created_by=user, created_at__date__gte=week_start).count(),
            'tickets_month': Ticket.objects.filter(created_by=user, created_at__date__gte=month_start).count(),
            'roles_tkts': roles_tkts,
            'categories': categories,
            'uncategorized_tickets': uncategorized_tickets,  # Tickets sem categoria
            'unknow_user':unknow_user,
            'usuarios': usuarios,
            'notifications': notifications,
            'work_schedule':work_schedule
        })

        return context
