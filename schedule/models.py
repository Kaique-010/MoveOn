from django.db import models
from move_on.models import User
from core import settings

class Event(models.Model):
    title = models.CharField("Titulo",max_length=255)
    description = models.TextField("Descrição",blank=True, null=True)
    start_time = models.DateTimeField("Inicio")
    end_time = models.DateTimeField("Fim")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.start_time} - {self.end_time})"
