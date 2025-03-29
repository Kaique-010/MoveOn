from django.urls import path
from .views import (MenuViewiew, TicketCreate, TicketDelete,
                    TicketDetail, TicketListView, TicketUpdate,
                    SlaList, SLACreateView, ParamsView)

urlpatterns = [
    path('menu', MenuViewiew.as_view(), name='index'), 
    path('params', ParamsView.as_view(), name='params'), 
    path('tickets/list',TicketListView.as_view(), name="ticket_list"),
    path('tickets/detail/<int:pk>', TicketDetail.as_view(), name="ticket_detail"),
    path('tickets/create', TicketCreate.as_view(), name="ticket_form"),
    path('tickets/update/<int:pk>', TicketUpdate.as_view(), name="ticket_update"),
    path('tickets/delete/<int:pk>', TicketDelete.as_view(), name="ticket_delete"),
    path('tickets/slalist', SlaList.as_view(), name="sla_list"),
    path('tickets/slacreate', SLACreateView.as_view(), name="sla_create"),
]
