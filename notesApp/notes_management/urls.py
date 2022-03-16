from django.urls import path

from notesApp.notes_management.views import create_note, NotesDetailView, update_note, \
    NotesDeleteView, delete_note, NotesListView

urlpatterns = [
    path('', NotesListView.as_view(), name="notes list"),
    path('create/', create_note, name="note create"),
    path('details/<int:pk>/', NotesDetailView.as_view(), name="note detail"),
    path('update/<int:pk>/', update_note, name="note update"),
    path('delete/<int:pk>/', delete_note, name="note delete"),
]
