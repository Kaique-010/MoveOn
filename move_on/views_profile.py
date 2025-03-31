from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse_lazy
from move_on.forms import ProfileForms
from .models import Profile


class ProfileListView(LoginRequiredMixin, ListView):
    model= Profile
    template_name = 'Profile/profile_list.html'
    context_object_name = 'profiles'
    

class ProfileCreateView(LoginRequiredMixin, CreateView):
    model= Profile
    template_name = 'Profile/profile_form.html'
    success_url = reverse_lazy("profile_list")
    form_class = ProfileForms
    
    def form_valid(self, form):
        return super().form_valid(form)

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model= Profile
    template_name = 'Profile/profile_form.html'
    success_url = reverse_lazy("profile_list")
    form_class = ProfileForms
    
    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)
   

class ProfileDeleteView(LoginRequiredMixin, DeleteView):
    model= Profile
    template_name = 'Profile/profile_delete.html'
    success_url = reverse_lazy("profile_list")
    
    

