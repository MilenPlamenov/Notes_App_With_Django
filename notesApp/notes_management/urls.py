from django.urls import path

from notesApp.notes_management.views import NotesListView, NoteCreate, NotesDetailView, NotesUpdateView, NotesDeleteView

urlpatterns = [
    path('', NotesListView.as_view(), name="notes list"),
    path('create/', NoteCreate.as_view(), name="note create"),
    path('<pk>/', NotesDetailView.as_view(), name="note detail"),
    path('update/<int:pk>/', NotesUpdateView.as_view(), name="note update"),
    path('delete/<int:pk>/', NotesDeleteView.as_view(), name="note delete"),
]