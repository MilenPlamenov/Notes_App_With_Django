from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import generic

from notesApp.notes_management.forms import CreateNote, EditNote, DeleteNote
from notesApp.notes_management.models import Note
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView


class NotesListView(generic.ListView):
    model = Note
    context_object_name = "notes"
    template_name = "notes_list.html"


def notes_list(request):
    context = {
        "notes": Note.objects.all()
    }
    return render(request, "notes_list.html", context)


class NoteCreate(CreateView):
    model = Note
    template_name = "create.html"
    success_url = '/'
    fields = ["subject", "text", "date"]

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        note = form.save(commit=False)
        note.user = self.request.user
        note.save()
        return redirect('notes list')


# def create_note(request):
#     if not request.user.is_authenticated:
#         return redirect("create profile")
#     if request.method == 'POST':
#         form = CreateNote(request.POST, request.FILES)
#         if form.is_valid():
#             note = form.save(commit=False)
#             note.user = request.user
#             note.save()
#             return redirect('notes list')
#     else:
#         form = CreateNote()
#
#     context = {
#         "form": form,
#     }
#
#     return render(request, 'create.html', context)


class NotesDetailView(DetailView):
    model = Note
    template_name = "details.html"


class NotesUpdateView(UpdateView):
    model = Note
    fields = ["subject", "text", "date"]
    success_url = "/"
    template_name = "update_notes.html"


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
    return render(request, "update_notes.html", context)


class NotesDeleteView(DeleteView):
    model = Note
    success_url = "/"
    template_name = "delete_notes.html"


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
    return render(request, "delete_notes.html", context)

