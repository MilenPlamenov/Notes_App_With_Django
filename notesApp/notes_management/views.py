from django.contrib import messages
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views import generic

from notesApp.notes_management.forms import CreateProfile, LoginProfile, CreateNote, EditNote, DeleteNote, EditProfile, \
    PasswordChange, DeleteProfile
from notesApp.notes_management.models import Note
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView


# class NotesListView(generic.ListView):
#     model = Note
#     context_object_name = "notes"
#     template_name = "notes_list.html"


def notes_list(request):
    context = {
        "notes": Note.objects.all()
    }
    return render(request, "notes_list.html", context)


# class NoteCreate(CreateView):
#     model = Note
#     template_name = "create.html"
#     success_url = '/'
#     fields = ["subject", "text", "date"]


def create_note(request):
    if not request.user.is_authenticated:
        return redirect("create profile")
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


def delete_profile(request, pk):
    profile = User.objects.get(pk=pk)
    if profile != request.user:
        return redirect("notes list")
    if not request.user.is_authenticated:
        return redirect('create profile')
    if request.method == "GET":
        form = DeleteProfile(instance=profile)
    else:
        form = DeleteProfile(request.POST, instance=profile)
        if form.is_valid():
            profile.delete()
            return redirect('create profile')
    context = {
        "form": form,
        "profile": profile,
    }

    return render(request, "delete_profile.html", context)


def change_password(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = PasswordChange(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('notes list')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChange(request.user)

    context = {
        "form": form,
    }
    return render(request, "change_password.html", context)
