from django.views.generic import ListView, CreateView, UpdateView
from django.urls import reverse_lazy
from work_schedule.models import WorkSchedule
from .forms import WorkScheduleForm

class WorkScheduleListView(ListView):
    model = WorkSchedule
    template_name = 'schedule/work_schedule_list.html'
    context_object_name = 'schedules'

class WorkScheduleCreateView(CreateView):
    model = WorkSchedule
    form_class= WorkScheduleForm
    template_name = 'schedule/work_schedule_form.html'
    success_url = reverse_lazy('work_schedule_list')

class WorkScheduleUpdateView(UpdateView):
    model = WorkSchedule
    form_class= WorkScheduleForm
    template_name = 'schedule/work_schedule_form.html'
    success_url = reverse_lazy('work_schedule_list')

class DayOffListView(ListView):
    model = WorkSchedule
    template_name = 'schedule/day_off_list.html'
    context_object_name = 'day_off_schedules'

    def get_queryset(self):
        return WorkSchedule.objects.filter(status='day_off')