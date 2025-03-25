import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import ChatRoom, Message

def chat_room(request, room_name):
    return render(request, "chat.html", {"room_name": room_name})

@csrf_exempt
def send_message(request):
    if request.method == "POST":
        try:
            room_name = request.POST.get("room")
            message = request.POST.get("message")
            
            if room_name and message:
                room = ChatRoom.objects.get(name=room_name)
                # Crie um objeto Message ou similar para armazenar a mensagem
                # Exemplo:
                # Message.objects.create(user=request.user, room=room, content=message)
                return JsonResponse({"status": "ok"})
            else:
                return JsonResponse({"status": "fail", "message": "Invalid data"})
        except Exception as e:
            return JsonResponse({"status": "fail", "message": str(e)})
    return JsonResponse({"status": "fail", "message": "Invalid method"})

def stream_messages(request, room_name):
    # Gerar uma resposta SSE
    room = ChatRoom.objects.get(name=room_name)
    
    def event_stream():
        for message in room.messages.all():
            yield f"data: {message.text}\n\n"
    
    response = HttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    response['Connection'] = 'keep-alive'
    return response


def get_or_create_room(request, room_name):
    # Verifica se a sala já existe
    room, created = ChatRoom.objects.get_or_create(name=room_name)
    
    # Se a sala foi criada, podemos adicionar algum código aqui para notificar ou fazer algo mais
    if created:
        print(f'Sala {room_name} criada com sucesso.')

    return render(request, 'chat/room.html', {'room_name': room.name})