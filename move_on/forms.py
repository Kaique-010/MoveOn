from django import forms
from .models import Ticket, TicketAlert, SLA

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'assigned_to', 'status', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ticket title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the issue'}),
            'assigned_to': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
        }

class TicketAlertForm(forms.ModelForm):
    class Meta:
        model = TicketAlert
        fields = ['ticket', 'message', 'webhook_url', 'api_endpoint']
        widgets = {
            'ticket': forms.Select(attrs={'class': 'form-select'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter alert message'}),
            'webhook_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter webhook URL'}),
            'api_endpoint': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter API endpoint'}),
        }
    


class SLAForm(forms.ModelForm):
    class Meta:
        model = SLA
        fields = ['priority', 'response_time', 'resolution_time']

    def clean(self):
        cleaned_data = super().clean()
        response_time = cleaned_data.get("response_time")
        resolution_time = cleaned_data.get("resolution_time")

        # Validar que o tempo de resolução não seja menor que o tempo de resposta
        if resolution_time and response_time and resolution_time < response_time:
            raise forms.ValidationError("O tempo de resolução não pode ser menor que o tempo de resposta.")
        return cleaned_data