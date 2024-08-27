from django.urls import path
from .views import AssignTasksReportView

urlpatterns = [
    path('assign/', AssignTasksReportView.as_view(), name='assign-tasks-report'),
]
