from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import send_message, stream_messages, get_or_create_room, send_audio, send_image

urlpatterns = [
    path('new', get_or_create_room, name='chat_new'),
    path("<int:ticket_id>/send/", send_message, name="send_message"),
    path("stream/<int:ticket_id>/", stream_messages, name="stream_messages"),
    path("<int:ticket_id>/send-audio/", send_audio, name="send_audio"),
    path("<int:ticket_id>/send-image/", send_image, name="send_image"),
] 

# Adicionar configuração de arquivos estáticos e de mídia
if settings.DEBUG:  # Certifique-se de que estamos em modo de desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
