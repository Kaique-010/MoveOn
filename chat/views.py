# tickets/views.py
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Ticket, TicketMessage

def ticket_chat_messages(request, ticket_id):
    """Retorna mensagens do chat para uma API REST"""
    ticket = get_object_or_404(Ticket, id=ticket_id)
    
    # Verificação de permissão similar ao consumer
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    messages = TicketMessage.objects.filter(ticket=ticket).order_by('created_at')
    
    data = {
        'messages': [
            {
                'id': msg.id,
                'author': msg.author.username,
                'content': msg.content,
                'created_at': msg.created_at.isoformat(),
                'is_read': msg.read_by.filter(id=request.user.id).exists()
            }
            for msg in messages
        ]
    }
    
    return JsonResponse(data)

def chat_room(request, room_name):
    return render(request, "chat.html", {"room_name": room_name})