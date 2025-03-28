import json
import time
from django.http import JsonResponse, HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import ChatRoom, Message
from move_on.models import SLA, SLAPriority, Team, Ticket
from collections import deque
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import os


def get_or_create_room(request):
    # Obter a instância do SLA com a prioridade LOW
    sla_instance = SLA.objects.get(priority=SLAPriority.LOW)
   
   #filtramos pela instancia de Team ao buscar o nome 
    default_team = Team.objects.filter(name="Técnicos").first()
    
    # Agora, associamos as instâncias ao criar o ticket
    ticket = Ticket.objects.create(
        client=None,
        sla=sla_instance,  # Passa a instância do SLA ao invés da string
        created_by = request.user if request.user.is_authenticated else None,
        assigned_team = default_team
    )
    
    room = ChatRoom.objects.create(ticket=ticket)
    
    print(f"sala criada para o {ticket.id} com SLA de prioridade {sla_instance.priority}")

    # Renderizamos a sala com o ID do ticket
    return render(request, 'chat.html', {'ticket_id': ticket.id})

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