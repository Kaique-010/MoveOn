from django import forms
from work_schedule.models import WorkSchedule

class WorkScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkSchedule
        fields = '__all__'
        widgets = {
            'worker': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'shift_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'override_day_off': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
