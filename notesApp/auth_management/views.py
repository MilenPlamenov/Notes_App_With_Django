from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, authenticate, login
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from notesApp.auth_management.forms import PasswordChange, EditExtendedProfile, EditProfile, LoginProfile, \
    CreateProfile, ProfileForm, DeleteExtendedProfile, DeleteProfile
from notesApp.tasks_management.models import Task


@transaction.atomic  # if one operation is invalid - all are
def create_profile(request):
    if request.method == "GET":
        user_form = CreateProfile()
        profile_form = ProfileForm()
    else:
        user_form = CreateProfile(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            login(request, user)
            return redirect('/')

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, 'profile/create_profile.html', context)


@transaction.atomic
def edit_profile(request):
    profile = request.user.get_username()
    if profile != request.user.username:
        return redirect("notes list")

    if request.method == "GET":
        user_form = EditProfile(instance=request.user)
        profile_form = EditExtendedProfile(instance=request.user.profile)
    else:
        user_form = EditProfile(request.POST, instance=request.user)
        profile_form = EditExtendedProfile(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect("notes list")

    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }
    return render(request, "profile/edit_profile.html", context)


class ProfileDetailView(DetailView):
    model = User
    template_name = "profile/profile_details.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return Task.objects.filter(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = Task.objects.get()
        # should fix this to show the tasks for each user !
        return context


def profile_details(request, pk):
    if not request.user.is_authenticated:
        return redirect('create profile')

    user = User.objects.get(pk=pk)
    context = {
        'user': user,
        'tasks': Task.objects.filter(user=user),
        'user_checker': user == request.user
        # check if that is the currently logged in user or the user is checking other profile
    }

    return render(request, "profile/profile_details.html", context)


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
    return render(request, "profile/login_profile.html", context)


@transaction.atomic
def delete_profile(request, pk):
    profile = User.objects.get(pk=pk)
    if profile != request.user:
        return redirect("notes list")
    if not request.user.is_authenticated:
        return redirect('create profile')
    if request.method == "GET":
        user_form = DeleteProfile(instance=request.user)
        profile_form = DeleteExtendedProfile(instance=request.user.profile)
    else:
        profile.delete()
        return redirect('create profile')
    context = {
        "user_form": user_form,
        "profile_form": profile_form,
    }

    return render(request, "profile/delete_profile.html", context)


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
    return render(request, "profile/change_password.html", context)
