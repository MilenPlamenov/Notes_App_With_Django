from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

from notesApp.auth_management.models import Profile


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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', 'description', 'birth')


class EditProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name")  # added first and last name / easier register in the app

    def __init__(self, *args, **kwargs):  # rewriting the init method to remove the help text from the fields
        super(EditProfile, self).__init__(*args, **kwargs)
        for field_name in ['username']:
            self.fields[field_name].help_text = None


class EditExtendedProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('description', 'birth', 'gender', 'image_url')


class DeleteProfile(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(DeleteProfile, self).__init__(*args, **kwargs)
        for field_name in ['username']:
            self.fields[field_name].help_text = None

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name",)
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'disabled': True,
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'disabled': True,
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    'disabled': True,
                }
            ),
        }


class DeleteExtendedProfile(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('description', 'birth', 'gender')
        widgets = {
            'description': forms.TextInput(
                attrs={
                    'disabled': True,
                }
            ),
            'birth': forms.TextInput(
                attrs={
                    'disabled': True,
                }
            ),
            "gender": forms.TextInput(
                attrs={
                    'disabled': True,
                }
            ),
        }


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


class PasswordChange(PasswordChangeForm):

    def __init__(self, *args, **kwargs):  # rewriting the init method to remove the help text from the fields
        super(PasswordChange, self).__init__(*args, **kwargs)
        for field_name in ['new_password1']:
            self.fields[field_name].help_text = None
