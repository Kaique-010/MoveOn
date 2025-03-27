from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('move/', include('move_on.urls')),
    path('chat/', include('chat.urls')),
    path('', include('accounts.urls'))
]


# Adicionar configuração de arquivos estáticos e de mídia
if settings.DEBUG:  # Certifique-se de que estamos em modo de desenvolvimento
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
