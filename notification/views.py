from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Notifications
from .forms import NotificationForm
from rest_framework import viewsets
from .serializers import NotificationSerializer

class NotificationListView(ListView):
    model = Notifications
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    ordering = ['-created_at']

class NotificationCreateView(CreateView):
    model = Notifications
    form_class = NotificationForm
    template_name = 'notifications/notification_form.html'
    success_url = reverse_lazy('notification_list')

class NotificationUpdateView(UpdateView):
    model = Notifications
    form_class = NotificationForm
    template_name = 'notifications/notification_form.html'
    success_url = reverse_lazy('notification_list')

class NotificationDeleteView(DeleteView):
    model = Notifications
    template_name = 'notifications/notification_confirm_delete.html'
    success_url = reverse_lazy('notification_list')





class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notifications.objects.all().order_by('-created_at')
    serializer_class = NotificationSerializer