from django.urls import path

from notesApp.tasks_management.views import TaskCreate

urlpatterns = [
    path('create/', TaskCreate.as_view(), name="task create"),
]