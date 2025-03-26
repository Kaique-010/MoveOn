from django.urls import path
from .views import send_message, stream_messages, get_or_create_room

urlpatterns = [
    path("<str:room_name>/", get_or_create_room, name="chat_room"),
    path("<str:room_name>/send/", send_message, name="send_message"),  # Adicionar room_name à URL
    path("stream/<str:room_name>/", stream_messages, name="stream_messages"),
]
