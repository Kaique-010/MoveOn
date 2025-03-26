import json
import time
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from .models import ChatRoom, Message
from collections import deque

# Usamos uma lista para armazenar as conexões ativas de SSE
active_connections = []

def send_message(request, room_name):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user if request.user.is_authenticated else None

            room, _ = ChatRoom.objects.get_or_create(name=room_name)
            message = Message.objects.create(room=room, user=user, text=data["message"])

            # Aqui você envia a mensagem para todas as conexões SSE
            for connection in active_connections:
                connection.write(f"data: {message.text}\n\n")
            
            # Retorna a resposta imediatamente para quem enviou a mensagem
            return JsonResponse({"status": "ok", "message": message.text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método não permitido"}, status=405)


def stream_messages(request, room_name):
    room = ChatRoom.objects.get(name=room_name)

    # Criar uma função para o stream de SSE
    def event_stream():
        last_message = None
        while True:
            room.refresh_from_db()  # Atualiza o objeto da sala para obter a última mensagem
            last_message_instance = room.messages.last()  # Verifique se está pegando a última mensagem corretamente
            if last_message_instance and last_message_instance.text != last_message:
                last_message = last_message_instance.text
                yield f"data: {last_message}\n\n"
            time.sleep(1)  # Aguarda um segundo antes de verificar novamente

    # Criar a resposta do evento
    response = HttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    response['Connection'] = 'keep-alive'

    # Adiciona essa conexão à lista de conexões ativas
    active_connections.append(response)
    
    # Remove a conexão da lista quando ela se desconectar
    def remove_connection():
        active_connections.remove(response)

    response.close = remove_connection

    return response


def get_or_create_room(request, room_name):
    room, created = ChatRoom.objects.get_or_create(name=room_name)
    if created:
        print(f'Sala {room_name} criada com sucesso.')

    return render(request, 'chat.html', {'room_name': room.name})
