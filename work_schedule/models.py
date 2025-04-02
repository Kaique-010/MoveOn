from datetime import timedelta
from django.db import models
from django.core.exceptions import ValidationError
from core import settings

class WorkShiftConfig(models.Model):
    worker = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    lunch_break_minutes = models.PositiveIntegerField(default=0)  
    work_days = models.JSONField(default=list)  # Ex: ["monday", "tuesday", "wednesday", "thursday", "friday"]
    max_weekly_hours = models.PositiveIntegerField(default=40)

    def __str__(self):
        return f"{self.worker} - {self.start_time} às {self.end_time} ({self.max_weekly_hours}h/semana)"


class WorkSchedule(models.Model):
    SHIFT_CHOICES = [
        ('morning', 'Manhã'),
        ('afternoon', 'Tarde'),
        ('night', 'Noite')
    ]
    
    STATUS_CHOICES= [
        ('active', 'Ativo'),
        ('day_off', 'Folga'),
        ('absent', 'Ausente')
    ]
    
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    shift_type = models.CharField(max_length=10, choices=SHIFT_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    override_day_off = models.BooleanField(default=False)  # Permite edição manual da folga
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('worker', 'date', 'start_time', 'end_time')
        ordering = ['date', 'start_time']
        db_table = 'workschedule'

    def clean(self):
        super().clean()
        
        if self.start_time >= self.end_time:
            raise ValidationError("O Horário de Início não pode ser maior ou igual ao horário de término")
        
        overlapping_shifts = WorkSchedule.objects.filter(
            worker=self.worker,
            date=self.date
        ).exclude(pk=self.pk).filter(
            models.Q(start_time__lt=self.end_time, end_time__gt=self.start_time)
        )
        
        if overlapping_shifts.exists():
            raise ValidationError("O trabalhador já possui um turno inserido neste dia")
    
    @classmethod
    def total_hours_week(cls, worker, week_start):
        """Calcula o total de horas trabalhadas em uma semana com base na jornada"""
        week_end = week_start + timedelta(days=6)
        schedules = cls.objects.filter(worker=worker, date__range=[week_start, week_end])
        total_seconds = sum(
            (schedule.end_time.hour * 3600 + schedule.end_time.minute * 60) -
            (schedule.start_time.hour * 3600 + schedule.start_time.minute * 60)
            for schedule in schedules
        )
        return total_seconds / 3600
    
    def set_day_off(self):
        from schedule.models import WorkShift  # Importação dentro do método para evitar import circular
        
        if self.override_day_off:
            return  # Se a folga for manual, não altera
        
        try:
            work_shift = WorkShift.objects.get(worker=self.worker)
            max_weekly_hours = work_shift.total_hours
        except WorkShift.DoesNotExist:
            max_weekly_hours = 40  # Valor padrão caso não tenha jornada definida
        
        if self.total_hours_week(self.worker, self.date - timedelta(days=self.date.weekday())) >= max_weekly_hours:
            self.status = 'day_off'
    
    def save(self, *args, **kwargs):
        self.clean()
        self.set_day_off()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.worker} - {self.date} ({self.get_shift_type_display()})"
