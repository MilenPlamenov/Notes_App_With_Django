from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DeleteView

from notesApp.tasks_management.models import Task


class TaskCreate(CreateView):
    model = Task
    template_name = "tasks/create_task.html"
    success_url = '/'
    fields = ["name", "text", "is_done", "image_url"]

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        task = form.save(commit=False)
        task.user = self.request.user
        task.save()
        return redirect('notes list')


class TaskUpdate(UpdateView):
    model = Task
    fields = ["name", "text", "is_done", "image_url"]
    success_url = "/"
    template_name = "tasks/edit_task.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    # getting the current note object
    def get_object(self, queryset=None):
        try:
            return super(TaskUpdate, self).get_object(queryset)
        except AttributeError:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return redirect('notes list')
        return super(TaskUpdate, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return redirect('notes list')
        return super(TaskUpdate, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return redirect("notes list")


class TaskDelete(DeleteView):
    model = Task
    success_url = "/"
    template_name = "tasks/delete_task.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return super(TaskDelete, self).get_object(queryset)
        except AttributeError:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return redirect('notes list')
        return super(TaskDelete, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return redirect('notes list')
        self.object.image_url.delete()
        self.object.delete()
        return redirect("notes list")
