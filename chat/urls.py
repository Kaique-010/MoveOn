
from django.urls import path
from . import views
from .views import chat_room

urlpatterns = [

    path('api/tickets/<int:ticket_id>/chat/', views.ticket_chat_messages, name='ticket_chat_messages'),
    path("chat/<str:room_name>/", chat_room, name="chat_room"),
]