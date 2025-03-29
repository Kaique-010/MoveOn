from datetime import timedelta
import json
import time
from django.http import JsonResponse, HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.db.models import Count
from django.core.files.base import ContentFile
from .models import Attendant, ChatQueue, ChatRoom, ChatSettings, Message
from django.views.generic import UpdateView, ListView, CreateView, DeleteView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.timezone import now
from django.urls import reverse_lazy
from .models import ChatSettings
from .forms import ChatSettingsForm
from move_on.models import SLA, SLAPriority, Team, Ticket, User
from collections import deque
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import os


def get_or_create_room(request, ticket_id=None):
    # Verifica se o cliente tem um ticket ativo
    if request.user.is_authenticated:
        if ticket_id:
            # Caso o ticket_id tenha sido passado, tenta buscar esse ticket
            active_ticket = Ticket.objects.filter(id=ticket_id, created_by=request.user, status__name='Em Andamento').first()
            if active_ticket:
                # Se já tem um ticket ativo, verifica se existe uma sala de chat associada
                room = ChatRoom.objects.filter(ticket=active_ticket).first()
                if room:
                    return render(request, 'chat.html', {'ticket_id': active_ticket.id, 'chat_room': room})
                else:
                    # Se não existir sala, cria uma nova sala de chat associada ao ticket
                    chat_room = ChatRoom.objects.create(ticket=active_ticket)
                    return render(request, 'chat.html', {'ticket_id': active_ticket.id, 'chat_room': chat_room})
            else:
                # Se o ticket não for encontrado ou não estiver ativo, cria um novo ticket e sala
                return create_new_ticket_and_room(request)
        else:
            # Caso não tenha o ticket_id na URL, cria um novo ticket e sala
            return create_new_ticket_and_room(request)
    
    # Se o usuário não estiver autenticado, redireciona ou retorna erro
    return render(request, 'error.html', {'message': 'Você precisa estar autenticado para acessar o chat.'})

def create_new_ticket_and_room(request):
    # Cria um novo ticket e sala de chat
    sla_instance = SLA.objects.get(priority=SLAPriority.LOW)
    default_team = Team.objects.filter(name="Técnicos").first()

    ticket = Ticket.objects.create(
        client=None,
        sla=sla_instance,
        created_by=request.user if request.user.is_authenticated else None,
        assigned_team=default_team
    )

    # Cria a sala de chat associada ao novo ticket
    chat_room = ChatRoom.objects.create(ticket=ticket)

    # Atribui o chat a um atendente
    chat_room = assign_chat_to_attendant(ticket)

    if chat_room:
        return render(request, 'chat.html', {'ticket_id': ticket.id, 'chat_room': chat_room})
    else:
        return render(request, 'chat_queued.html', {'ticket_id': ticket.id})



def send_message(request, ticket_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user if request.user.is_authenticated else None

            room = get_object_or_404(ChatRoom, ticket__id=ticket_id)
            message = Message.objects.create(room=room, user=user, text=data["message"])

            return JsonResponse({"status": "ok", "message": message.text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método não permitido"}, status=405)

def stream_messages(request, ticket_id):
    try:
        room = ChatRoom.objects.get(ticket__id=ticket_id)
    except ChatRoom.DoesNotExist:
        return HttpResponse("Sala não encontrada", status=404)

    def event_stream():
        last_message = None
        while True:
            try:
                room.refresh_from_db()
                last_message_instance = room.messages.last()

                if last_message_instance and last_message_instance.text != last_message:
                    last_message = last_message_instance.text
                    sender = "user" if last_message_instance.user == room.ticket.client else "attendant"
                    
                    # Nome do remetente
                    if sender == "user":
                        sender_name = room.ticket.client.user.username
                    else:
                        sender_name = last_message_instance.user.username

                    # Emite os dados da mensagem para o cliente
                    yield f"data: {json.dumps({'message': last_message, 'sender': sender, 'sender_name': sender_name})}\n\n"
                
                time.sleep(1)
            except Exception as e:
                print(f"Erro no SSE: {e}")
                break

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'

    return response

#Função para envio de Audios
@csrf_exempt
def send_audio(request, ticket_id):
    if request.method == "POST" and request.FILES.get('audio'):
        try:
            audio_file = request.FILES['audio']
            audio_path = default_storage.save(f'audios/{ticket_id}.wav', ContentFile(audio_file.read()))
            audio_url = default_storage.url(audio_path)

            return JsonResponse({
                "status": "ok",
                "sender": "user",
                "sender_name": "Usuário",
                "audio_url": audio_url  
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Áudio não enviado ou método não permitido."}, status=400)

#função para enviar prints
@csrf_exempt
def send_image(request, ticket_id):
    if request.method == "POST":
        if "image" in request.FILES:
            image = request.FILES["image"]
            print(f"Imagem recebida: {image.name}") 
        else:
            print("Nenhuma imagem foi enviada.") 

        if "image" in request.FILES:
           
            upload_dir = "uploads/chat_images/"
            file_path = os.path.join(upload_dir, f"{ticket_id}_{image.name}")
            saved_path = default_storage.save(file_path, ContentFile(image.read()))
            file_url = default_storage.url(saved_path)

            return JsonResponse({
                "status": "ok",
                "sender": "user",
                "sender_name": request.user.username,
                "file_url": file_url
            })

        return JsonResponse({"status": "error", "message": "Nenhuma imagem foi enviada"}, status=400)



def assign_chat_to_attendant(ticket):
    """ Atribui um chat a um atendente seguindo as regras definidas. """

    settings = ChatSettings.objects.filter(client=ticket.client).first()
    team = ticket.assigned_team

    if not settings or not team:
        return None  # Sem configuração ou equipe, não faz nada

    # Busca atendentes disponíveis do time
    attendants = Attendant.objects.filter(team=team, available=True)

    if settings.balance_tickets:
        # Ordena os atendentes pelo número de tickets já atribuídos
        attendants = sorted(attendants, key=lambda a: a.user.created_tickets.count())

    # Filtra os atendentes que ainda podem receber tickets
    attendants = [a for a in attendants if a.user.created_tickets.count() < settings.max_tickets_per_attendant]

    if attendants:
        # Pega o primeiro atendente disponível
        attendant = attendants[0]
        chat_room, created = ChatRoom.objects.get_or_create(ticket=ticket)

        # Marca o atendente como ocupado se for distribuição automática
        if settings.auto_assign:
            attendant.available = False
            attendant.save()

        return chat_room

    # Se não há atendente disponível, coloca na fila
    ChatQueue.objects.get_or_create(ticket=ticket)
    return None

def release_attendant(attendant):
    """ Libera um atendente e atribui o próximo da fila, se houver. """

    attendant.available = True
    attendant.save()

    next_in_queue = ChatQueue.objects.first()
    if next_in_queue:
        assign_chat_to_attendant(next_in_queue.ticket)
        next_in_queue.delete()



def queue_status_stream(request):
    def event_stream():
        while True:
            queue_size = ChatQueue.objects.count()
            yield f"data: {queue_size}\n\n"
            time.sleep(2)

    return StreamingHttpResponse(event_stream(), content_type="text/event-stream")



class ChatSettingsView(LoginRequiredMixin, UpdateView):
    model = ChatSettings
    form_class = ChatSettingsForm
    template_name = "chat_settings.html"
    success_url = reverse_lazy("chat_settings")  # Redirecionamento pós-salvar

    def get_object(self, queryset=None):
        """ Retorna a configuração da empresa do usuário logado ou cria uma nova se não existir """
        chat_settings, created = ChatSettings.objects.get_or_create(client=self.request.user.client)
        return chat_settings



class ChatPanel(LoginRequiredMixin, TemplateView):
    template_name = 'chat_admin_painel.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        time_threshold = now() - timedelta(minutes=5)  # Considera online se ativo nos últimos 5 min

        attendants = User.objects.filter(role__name="Atendente")
        online_attendants = attendants.filter(last_login__gte=time_threshold)
        offline_attendants = attendants.filter(last_login__lt=time_threshold)

        # Contar atendimentos e listar clientes atendidos por cada atendente
        attendants_data = attendants.annotate(total_tickets=Count('created_tickets')).values('id', 'username', 'total_tickets')

        # Criar um dicionário para mapear atendentes aos clientes atendidos
        attendant_clients = {a.id: list(Ticket.objects.filter(created_by=a).values_list('client__name', flat=True).distinct()) for a in attendants}

        context.update({
            "online_attendants": online_attendants,
            "offline_attendants": offline_attendants,
            "attendants_data": attendants_data,
            "attendant_clients": attendant_clients,
        })
        return context


class ClientTicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = "client_tickets.html"
    context_object_name = "tickets"

    def get_queryset(self):
        return Ticket.objects.filter(client=self.request.user.client)
    


# Lista de atendentes
class AttendantListView(LoginRequiredMixin, ListView):
    model = Attendant
    template_name = 'attendant_list.html'
    context_object_name = 'attendants'

    def get_queryset(self):
        return Attendant.objects.all()

# Criação de um novo atendente
class AttendantCreateView(LoginRequiredMixin, CreateView):
    model = Attendant
    template_name = 'attendant_create.html'
    fields = ['user', 'team', 'available']
    success_url = reverse_lazy('attendant_list')  # Redireciona para a lista após criar

    def form_valid(self, form):
        # Certifica-se que o usuário logado é o criador
        form.instance.created_by = self.request.user
        return super().form_valid(form)

# Atualização da disponibilidade do atendente
class AttendantUpdateView(LoginRequiredMixin, UpdateView):
    model = Attendant
    template_name = 'attendant_update.html'
    fields = ['available']
    context_object_name = 'attendant'

    def get_success_url(self):
        return reverse_lazy('attendant_list')

# Exclusão de um atendente
class AttendantDeleteView(LoginRequiredMixin, DeleteView):
    model = Attendant
    template_name = 'attendant_confirm_delete.html'
    context_object_name = 'attendant'
    success_url = reverse_lazy('attendant_list')