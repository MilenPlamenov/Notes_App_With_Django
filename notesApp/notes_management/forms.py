from django import forms
from notesApp.notes_management.models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["subject", "text", "date"]


class CreateNote(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["subject", "text", "date", "image_url"]
        labels = {
            "image_url": "Image for your note",

        }


class EditNote(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["subject", "text", "date", "image_url"]
        labels = {
            "image_url": "Image for your note",

        }


class DeleteNote(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["subject", "text", "date"]


