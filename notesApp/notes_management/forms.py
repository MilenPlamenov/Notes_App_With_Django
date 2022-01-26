from django import forms

from notesApp.notes_management.models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["subject", "text", "date"]