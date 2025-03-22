from django.urls import path
from .views import MenuViewiew, TicketCreate, TicketDelete, TicketDetail, TicketListView, TicketUpdate, SlaList, SLACreateView

urlpatterns = [
    path('', MenuViewiew.as_view(), name='index'), 
    path('tickets/list',TicketListView.as_view(), name="ticket_list"),
    path('tickets/detail', TicketDetail.as_view(), name="ticket_detail"),
    path('tickets/create', TicketCreate.as_view(), name="ticket_form"),
    path('tickets/update', TicketUpdate.as_view(), name="ticket_detail"),
    path('tickets/delete', TicketDelete.as_view(), name="ticket_delete"),
    path('tickets/slalist', SlaList.as_view(), name="sla_list"),
    path('tickets/slacreate', SLACreateView.as_view(), name="sla_create"),
]
