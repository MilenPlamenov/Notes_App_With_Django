from django.urls import path

from notesApp.notes_management.views import NoteCreate, NotesDetailView, update_note, \
    NotesDeleteView, delete_note, NotesListView, NotesUpdateView

urlpatterns = [
    path('', NotesListView.as_view(), name="notes list"),
    # path('create/', create_note, name="note create"),
    path('create/', NoteCreate.as_view(), name="note create"),
    path('details/<int:pk>/', NotesDetailView.as_view(), name="note detail"),
    path('update/<int:pk>/', NotesUpdateView.as_view(), name="note update"),
    path('delete/<int:pk>/', delete_note, name="note delete"),
]
