from django.shortcuts import redirect
from django.views.generic import CreateView

from notesApp.tasks_management.models import Task


class TaskCreate(CreateView):
    model = Task
    template_name = "tasks/create_task.html"
    success_url = '/'
    fields = ["name", "text", "is_done"]

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        return redirect('notes list')

# TODO Making random task taker with {{ value|random }} 4 fun
