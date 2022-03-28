from django.views.generic import CreateView

from notesApp.tasks_management.models import Task


class TaskCreate(CreateView):
    model = Task
    template_name = "tasks/create_task.html"
    success_url = '/'
    fields = ["name", "text", "is_done"]
