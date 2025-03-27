import json
import time
from django.http import JsonResponse, HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import ChatRoom, Message
from move_on.models import SLA, SLAPriority, Ticket
from collections import deque
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
import os


def get_or_create_room(request):
    # Obter a instância do SLA com a prioridade LOW
    sla_instance = SLA.objects.get(priority=SLAPriority.LOW)
    
    # Agora, associamos a instância do SLA ao criar o ticket
    ticket = Ticket.objects.create(
        client=None,
        #created_by=user,  # Aqui você pode preencher o usuário quando disponível
        sla=sla_instance  # Passa a instância do SLA ao invés da string
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
        """chamamos o objeto de ultima mensagem de ChatRoom para fazer um loop, se enquanto o estiver passando 
        MEnsagens refresh no banco aguarda um segundo para passar a próxima mensagem 
        passa os dados em json 
        """
        last_message = None
        while True:
            try:
                room.refresh_from_db()
                last_message_instance = room.messages.last()

                if last_message_instance and last_message_instance.text != last_message:
                    last_message = last_message_instance.text
                    sender = "user" if last_message_instance.user == room.ticket.client else "attendant"
                    
                    # Defina o nome para o remetente
                    if sender == "user":
                        sender_name = room.ticket.client.user.username  # Nome do cliente
                    else:
                        sender_name = last_message_instance.user.username  # Nome do atendente

                    yield f"data: {json.dumps({'message': last_message, 'sender': sender, 'sender_name': sender_name})}\n\n"
                
                time.sleep(1)
            except Exception as e:
                print(f"Erro no SSE: {e}")
                break
        """Aqui ocorre o refresh    em StreamingHttpREsponse onde mantém a sala e a conversa aberta"""
    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'

    
    return response



@csrf_exempt
def send_audio(request, ticket_id):
    if request.method == "POST":
        try:
            # Lê o conteúdo da requisição
            data = json.loads(request.body.decode('utf-8'))
            audio_url = data.get('audio')  # Pega a URL do áudio que foi enviada

            if not audio_url:
                return JsonResponse({"status": "error", "message": "Áudio não enviado."}, status=400)

            # Aqui, você pode armazenar o áudio no banco de dados ou fazer o que for necessário.
            # No caso, estamos apenas retornando a URL do áudio.

            return JsonResponse({
                "status": "ok",
                "sender": "user",
                "sender_name": "Usuário",
                "audio_url": audio_url  # Retorna a URL do áudio
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Método não permitido."}, status=405)


@csrf_exempt
def send_image(request, ticket_id):
    if request.method == "POST":
        image_data = request.POST.get("image")  # Aqui você pega a imagem enviada
        # Salve a imagem e retorne a URL ou o caminho do arquivo

        # Faça o processamento da imagem (armazenamento, etc)
        return JsonResponse({"status": "ok", "sender": "user", "sender_name": request.user.username, "file_url": "image_url"})