from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from rest_framework.generics import ListAPIView
from django.urls import reverse_lazy
from .models import Event
from .forms import EventForm
from .serializer import EventSerializer

class EventListView(ListView):
    model = Event
    template_name = 'Events/event_list.html'
    context_object_name = 'events'
    
    

class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = 'Events/event_form.html'
    success_url = reverse_lazy('event_list')
    
    def form_valid(self, form):
        
        form.instance.user = self.request.user
        return super().form_valid(form)

class EventUpdateView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'Events/event_form.html'
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)


class EventDeleteView(DeleteView):
    model = Event
    template_name = 'Events/event_confirm_delete.html'
    success_url = reverse_lazy('event_list')


class EventListAPI(ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer