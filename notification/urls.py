from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    NotificationListView, NotificationCreateView,
    NotificationUpdateView, NotificationDeleteView, NotificationViewSet
)


router = DefaultRouter()
router.register(r'notifications', NotificationViewSet)

urlpatterns = [
    path('list', NotificationListView.as_view(), name='notification_list'),
    path('novo/', NotificationCreateView.as_view(), name='notification_form'),
    path('editar/<int:pk>/', NotificationUpdateView.as_view(), name='notification_edit'),
    path('excluir/<int:pk>/', NotificationDeleteView.as_view(), name='notification_delete'),
    path('api/', include(router.urls)),  # API REST para os avisos
    
]
