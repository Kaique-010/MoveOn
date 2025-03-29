from django import forms
from .models import ChatSettings

class ChatSettingsForm(forms.ModelForm):
    class Meta:
        model = ChatSettings
        fields = ["auto_assign", "balance_tickets", "max_tickets_per_attendant"]
