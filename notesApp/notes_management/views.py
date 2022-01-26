from django.views import generic

from notesApp.notes_management.models import Note
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView


class NotesListView(generic.ListView):
    model = Note
    context_object_name = "notes"
    template_name = "notes_list.html"


class NoteCreate(CreateView):
    model = Note
    template_name = "create.html"
    success_url = '/'
    fields = ["subject", "text", "date"]


class NotesDetailView(DetailView):
    model = Note
    template_name = "details.html"


class NotesUpdateView(UpdateView):
    model = Note
    fields = ["subject", "text", "date"]
    success_url = "/"
    template_name = "update_notes.html"


class NotesDeleteView(DeleteView):
    model = Note
    success_url ="/"
    template_name = "delete_notes.html"


# class based views for model -> Note with CRUD operations and list display
