from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from notesApp.notes_management.models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["subject", "text", "date"]


class CreateProfile(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter username',

                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(CreateProfile, self).__init__(*args, **kwargs)
        for field_name in ['username', 'password1', 'password2']:
            self.fields[field_name].help_text = None

        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': "Enter password"})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': "Confirm password"})
        # can't use attrs like the username so making it in the init method


class EditProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username",)


class CreateNote(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["subject", "text", "date", "image_url"]


class EditNote(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["subject", "text", "date"]


class DeleteNote(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["subject", "text", "date"]


class LoginProfile(forms.ModelForm):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "password")
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter your username',

                }
            ),
        }

    def __init__(self, *args, **kwargs):  # rewriting the init method to remove the help text from the fields
        super(LoginProfile, self).__init__(*args, **kwargs)
        for field_name in ['username']:
            self.fields[field_name].help_text = None

        self.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': "Enter your password"})

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data["username"]
            password = self.cleaned_data["password"]
            if not authenticate(username=username, password=password):
                raise forms.ValidationError("Invalid credentials")
