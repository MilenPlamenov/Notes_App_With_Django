from django.shortcuts import redirect, render
from django.views import generic

from notesApp.notes_management.forms import CreateNote, EditNote, DeleteNote
from notesApp.notes_management.models import Note
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView


# 1st cbv
class NotesListView(generic.ListView):
    model = Note
    context_object_name = "notes"
    template_name = "notes_list.html"


def notes_list(request):
    context = {
        "notes": Note.objects.all()
    }
    return render(request, "notes_list.html", context)


# 2nd cbv
class NoteCreate(CreateView):
    model = Note
    template_name = "notes/create.html"
    success_url = '/'
    fields = ["subject", "text", "date", "image_url"]

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        note = form.save(commit=False)
        note.user = self.request.user
        note.save()
        return redirect('notes list')


# 3rd cbv
class NotesDetailView(DetailView):
    model = Note
    template_name = "notes/details.html"


# 4th cbv
class NotesUpdateView(UpdateView):
    model = Note
    fields = ["subject", "text", "date", "image_url"]
    success_url = "/"
    template_name = "notes/update_notes.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    # getting the current note object
    def get_object(self, queryset=None):
        try:
            return super(NotesUpdateView, self).get_object(queryset)
        except AttributeError:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return redirect('notes list')
        return super(NotesUpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return redirect('notes list')
        return super(NotesUpdateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return redirect("notes list")


def update_note(request, pk):
    if not request.user.is_authenticated:
        return redirect("create profile")
    note = Note.objects.get(pk=pk)
    if note.user != request.user:
        return redirect("notes list")
    if request.method == "GET":
        form = EditNote(instance=note)
    else:
        form = EditNote(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            return redirect("notes list")
    context = {
        "form": form,
        "note": note,
    }
    return render(request, "notes/update_notes.html", context)


# 5th cbv
class NotesDeleteView(DeleteView):
    model = Note
    success_url = "/"
    template_name = "notes/delete_notes.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            return super(NotesDeleteView, self).get_object(queryset)
        except AttributeError:
            return None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return redirect('notes list')
        return super(NotesDeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.user != request.user:
            return redirect('notes list')
        self.object.image_url.delete()
        self.object.delete()
        return redirect("notes list")


def delete_note(request, pk):
    if not request.user.is_authenticated:
        return redirect("create profile")
    note = Note.objects.get(pk=pk)

    if note.user != request.user:
        return redirect("notes list")
    if request.method == "GET":
        form = DeleteNote()
    else:
        note.image_url.delete()
        note.delete()
        return redirect("notes list")

    context = {
        "form": form,
        "note": note,
    }
    return render(request, "notes/delete_notes.html", context)