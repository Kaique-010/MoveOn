from django.urls import path
from .views import (CategoriesDelete, CategoriesUpdate, CategoryCreate, CategoryList, MenuViewiew, SlaDeleteView, SlaUpdateView, TicketCreate, TicketDelete,
                    TicketDetail, TicketListView, TicketUpdate,
                    SlaList, SLACreateView, ParamsView)
from .views_profile import (ProfileDeleteView, ProfileListView, ProfileCreateView, ProfileUpdateView
     
)

urlpatterns = [
    path('menu', MenuViewiew.as_view(), name='index'), 
    path('params', ParamsView.as_view(), name='params'), 
    path('tickets/list',TicketListView.as_view(), name="ticket_list"),
    path('tickets/detail/<int:pk>', TicketDetail.as_view(), name="ticket_detail"),
    path('tickets/create', TicketCreate.as_view(), name="ticket_form"),
    path('tickets/update/<int:pk>', TicketUpdate.as_view(), name="ticket_update"),
    path('tickets/delete/<int:pk>', TicketDelete.as_view(), name="ticket_delete"),
    
    path('SLA/list', SlaList.as_view(), name="sla_list"),
    path('SLA/create', SLACreateView.as_view(), name="sla_form"),
    path('SLA/update/<int:pk>', SlaUpdateView.as_view(), name="sla_update"),
    path('SLA/delete/<int:pk>', SlaDeleteView.as_view(), name="sla_delete"),
    
    path('Category/list', CategoryList.as_view(), name='categories_list'),
    path('Category/create/', CategoryCreate.as_view(), name='category_form'),
    path('Category/update/<int:pk>', CategoriesUpdate.as_view(), name='category_update'),
    path('Category/delete/<int:pk>', CategoriesDelete.as_view(), name='category_delete'),
    
    path('Profile/list', ProfileListView.as_view(), name='profile_list'),
    path('Profile/create', ProfileCreateView.as_view(), name='profile_form'),
    path('Profile/delete/<int:pk>', ProfileDeleteView.as_view(), name='profile_delete'),
    path('Profile/update/<int:pk>', ProfileUpdateView.as_view(), name='profile_update'),
    
]
