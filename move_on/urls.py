from django.urls import path
from .views import (CategoriesDelete, CategoriesUpdate, CategoryCreate,
                    CategoryList, MenuViewiew, SlaDeleteView,
                    SlaUpdateView, StatusTicketCreateView, StatusTicketDeleteView,
                    StatusTicketListView, StatusTicketUpdateView, TeamCreateView,
                    TeamDeleteView, TeamList, TeamUpdateView, TicketCreate, TicketDelete,
                    TicketDetail, TicketListView, TicketUpdate,
                    UserListView, UserCreateView, UserUpdateView, UserDeleteView,
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
    
    path('Status/list', StatusTicketListView.as_view(), name='status_list'),
    path('Status/create', StatusTicketCreateView.as_view(), name='status_form'),
    path('Status/<int:pk>/delete', StatusTicketDeleteView.as_view(), name='status_delete'),
    path('Status/update/<int:pk>', StatusTicketUpdateView.as_view(), name='status_update'),
    
    path('Team/list', TeamList.as_view(), name='team_list'),
    path('Team/create', TeamCreateView.as_view(), name='team_form'),
    path('Team/delete/<int:pk>', TeamDeleteView.as_view(), name='team_delete'),
    path('Team/update/<int:pk>', TeamUpdateView.as_view(), name='team_update'),
    
    path("users/list", UserListView.as_view(), name="user_list"),
    path("users/create/", UserCreateView.as_view(), name="user_form"),
    path("users/update/<int:pk>/", UserUpdateView.as_view(), name="user_update"),
    path("users/delete/<int:pk>/", UserDeleteView.as_view(), name="user_delete"),
    
]
