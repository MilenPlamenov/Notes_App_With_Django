from django.urls import path

from notesApp.tasks_management.views import TaskCreate, TaskUpdate, TaskDelete

urlpatterns = [
    path('create/', TaskCreate.as_view(), name="task create"),
    path('edit/<int:pk>/', TaskUpdate.as_view(), name="task update"),
    path('delete/<int:pk>/', TaskDelete.as_view(), name="task delete"),
]
