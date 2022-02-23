from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import generic

from notesApp.notes_management.forms import CreateProfile, LoginProfile, CreateNote, EditNote, DeleteNote, EditProfile
from notesApp.notes_management.models import Note
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView


# class NotesListView(generic.ListView):
#     model = Note
#     context_object_name = "notes"
#     template_name = "notes_list.html"


def notes_list(request):
    if not request.user.is_authenticated:
        return redirect("create profile")
    notes = Note.objects.filter(user=request.user)

    context = {
        "notes": notes,

    }
    return render(request, "notes_list.html", context)


# class NoteCreate(CreateView):
#     model = Note
#     template_name = "create.html"
#     success_url = '/'
#     fields = ["subject", "text", "date"]


def create_note(request):
    if request.method == 'POST':
        form = CreateNote(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            return redirect('notes list')
    else:
        form = CreateNote()

    context = {
        "form": form,
    }

    return render(request, 'create.html', context)


class NotesDetailView(DetailView):
    model = Note
    template_name = "details.html"


class NotesUpdateView(UpdateView):
    model = Note
    fields = ["subject", "text", "date"]
    success_url = "/"
    template_name = "update_notes.html"


def update_note(request, pk):
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
    if request.method == "GET":
        pass
    else:
        pass

    context = {}
    return render(request, "delete_notes.html", context)


def delete_note(request, pk):
    note = Note.objects.get(pk=pk)
    if note.user != request.user:
        return redirect("notes list")
    if request.method == "GET":
        form = DeleteNote()
    else:
        note.delete()
        return redirect("notes list")

    context = {
        "form": form,
        "note": note,
    }
    return render(request, "delete_notes.html", context)


def create_profile(request):
    if request.method == "GET":
        form = CreateProfile()
    else:
        form = CreateProfile(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('notes list')

    context = {
        "form": form,
    }
    return render(request, 'create_profile.html', context)


def edit_profile(request, pk):
    profile = User.objects.get(pk=pk)
    if profile != request.user:
        return redirect("notes list")

    if request.method == "GET":
        form = EditProfile(instance=profile)
    else:
        form = EditProfile(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("notes list")

    context = {
        "form": form,
    }
    return render(request, "edit_profile.html", context)


def login_view(request):
    user = request.user

    if user.is_authenticated:
        return redirect('notes list')

    if request.method == 'GET':
        form = LoginProfile()
    else:
        form = LoginProfile(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            account = authenticate(username=username, password=password)
            if account:
                login(request, account)
                return redirect('notes list')
    context = {
        "form": form,
    }
    return render(request, "login_profile.html", context)
