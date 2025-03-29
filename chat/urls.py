from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import AttendantCreateView, AttendantDeleteView, AttendantListView, AttendantUpdateView, ChatPanel, ChatSettingsView, ClientTicketListView, send_message, stream_messages, get_or_create_room, send_audio, send_image

urlpatterns = [
    path('new', get_or_create_room, name='chat_new'),
    path("<int:ticket_id>/send/", send_message, name="send_message"),
    path('<int:ticket_id>/stream/', stream_messages, name='stream_messages'), 
    path("<int:ticket_id>/send-audio/", send_audio, name="send_audio"),
    path("<int:ticket_id>/send_image/", send_image, name="send_image"),
    path('config/chat/', ChatSettingsView.as_view(), name="chat_settings"),
    path('admin/chat/', ChatPanel.as_view(), name="chat_admin_panel"),
    path("meus-tickets/", ClientTicketListView.as_view(), name="client_tickets"),
    path('attendants/', AttendantListView.as_view(), name='attendant_list'),
    path('attendant/create/', AttendantCreateView.as_view(), name='attendant_create'),
    path('attendant/update/<int:pk>/', AttendantUpdateView.as_view(), name='attendant_update'),
    path('attendant/delete/<int:pk>/', AttendantDeleteView.as_view(), name='attendant_delete'),
]

# Adicionar configuração de arquivos estáticos e de mídia
if settings.DEBUG:  # Certifique-se de que estamos em modo de desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
