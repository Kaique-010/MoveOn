import json
import time
from django.http import JsonResponse, HttpResponse
from django.http import StreamingHttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from .models import ChatRoom, Message
from collections import deque



def send_message(request, room_name):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user = request.user if request.user.is_authenticated else None

            room = get_object_or_404(ChatRoom, name=room_name)  # Agora levanta erro 404 se a sala não existir
            message = Message.objects.create(room=room, user=user, text=data["message"])

            return JsonResponse({"status": "ok", "message": message.text})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método não permitido"}, status=405)


def stream_messages(request, room_name):
    try:
        room = ChatRoom.objects.get(name=room_name)
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
                    yield f"data: {json.dumps({'message': last_message})}\n\n"
                
                time.sleep(1)
            except Exception as e:
                print(f"Erro no SSE: {e}")
                break

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'

    
    return response


def get_or_create_room(request, room_name):
    room, created = ChatRoom.objects.get_or_create(name=room_name)
    if created:
        print(f'Sala {room_name} criada com sucesso.')

    return render(request, 'chat.html', {'room_name': room.name})
