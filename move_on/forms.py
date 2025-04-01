from tkinter import Widget
from attr import field
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Category, Team, Ticket, TicketAlert, SLA, Profile, TicketStatus, User

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'assigned_team', 'status', 'due_date', 'sla', 'client', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Entre com o Titulo geral do Tkt'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Descreva quais são os problemas'}),
            'assigned_team': forms.Select(attrs={'class': 'form-select'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'due_date': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'sla': forms.Select(attrs={'class': 'form-select'}),
            'client': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class':'form-select', 'placeholder': 'Categorias'}),
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

class CategoryForm(forms.ModelForm):
    class Meta:
        model= Category
        fields='__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Descrição'}),
        }

class ProfileForms(forms.ModelForm):
    document = forms.CharField(
        max_length=18,  # Mantém o mesmo limite do modelo
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CPF/CNPJ'})
    )

    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefone'}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TicketStatusForm(forms.ModelForm):
    
    class Meta:
        model= TicketStatus
        fields= '__all__'
        wigdets= {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
        }

class TeamForm(forms.ModelForm):
    
    class Meta:
        model=Team
        fields= '__all__'
        Widgets= {
            'client':forms.Select(attrs={'class': 'form-control', 'placeholder': 'cliente'}),
            'name':forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome'}),
            'roles':forms.Select(attrs={'class': 'form-control', 'placeholder': 'permissões'}),
            'members':forms.Select(attrs={'class': 'form-control', 'placeholder': 'membros'}),
            
        }
    
    

# Formulário para criação de usuário
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'client', 'role', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# 🔹 Formulário para atualização de usuário
class UserUpdateForm(UserChangeForm):
    password = None  # Esconde o campo de senha na edição

    class Meta:
        model = User
        fields = ['username', 'email', 'client', 'role', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'client': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }