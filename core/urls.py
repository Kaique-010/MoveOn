from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('move/', include('move_on.urls')),
    path('', include('accounts.urls'))
]
