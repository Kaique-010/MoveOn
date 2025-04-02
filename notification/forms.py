from django import forms
from .models import Notifications

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notifications
        fields = ['resume', 'redator', 'recipients']
        widgets = {
            'resume': forms.Textarea(attrs={'class': 'form-control'}),
            'redator': forms.Select(attrs={'class': 'form-control'}),
            'recipients': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
