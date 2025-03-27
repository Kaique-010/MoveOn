from django.urls import path
from .views import send_message, stream_messages, get_or_create_room

urlpatterns = [
    path('new', get_or_create_room, name='chat_new'),
    path("<int:ticket_id>/send/", send_message, name="send_message"), 
    path("stream/<int:ticket_id>/", stream_messages, name="stream_messages"),
]
