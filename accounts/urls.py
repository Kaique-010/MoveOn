from django.urls import path
from .views import custom_login, IndexView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('accounts/login/', custom_login, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', IndexView.as_view(), name='menu'), 
]
