from django.urls import path
from .views import WorkScheduleListView, WorkScheduleCreateView, WorkScheduleUpdateView, DayOffListView

urlpatterns = [
    path('work-schedules/', WorkScheduleListView.as_view(), name='work_schedule_list'),
    path('work-schedules/create/', WorkScheduleCreateView.as_view(), name='work_schedule_create'),
    path('work-schedules/<int:pk>/edit/', WorkScheduleUpdateView.as_view(), name='work_schedule_edit'),
    path('day-offs/', DayOffListView.as_view(), name='day_off_list'),
]
