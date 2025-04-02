from django.urls import path
from .views import EventListView, EventCreateView, EventUpdateView, EventDeleteView, EventListAPI

urlpatterns = [
    path('list', EventListView.as_view(), name='event_list'),
    path('novo/', EventCreateView.as_view(), name='event_form'),
    path('<int:pk>/editar/', EventUpdateView.as_view(), name='event_update'),
    path('<int:pk>/deletar/', EventDeleteView.as_view(), name='event_delete'),
    path('api/events/', EventListAPI.as_view(), name='api_events'),
]
