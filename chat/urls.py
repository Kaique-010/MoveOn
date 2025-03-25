# chat/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('<str:room_name>/', views.get_or_create_room, name='get_or_create_room'),
    path('send/', views.send_message, name='send_message'),
    path('stream/<str:room_name>/', views.stream_messages, name='stream_messages'),
    # Outras URLs, se necessário
]
