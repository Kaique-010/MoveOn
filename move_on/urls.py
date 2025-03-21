from django.urls import path
from .views import MenuViewiew

urlpatterns = [
    path('', MenuViewiew.as_view(), name='index'), 
]