from django.db import models
from core import settings

class Notifications(models.Model):
    resume = models.TextField('Aviso')
    redator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    recipients = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="notification_recipients", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.resume[:50]  

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ["-created_at"]  # Ordena da mais recente para a mais antiga
        db_table = 'notifications'
