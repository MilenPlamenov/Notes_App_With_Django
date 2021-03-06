from django.urls import path

from notesApp.notes_management.views import NotesCreateView, NotesDetailView, \
    NotesDeleteView, NotesListView, NotesUpdateView

urlpatterns = [
    path('', NotesListView.as_view(), name="notes list"),
    # path('create/', create_note, name="note create"),
    path('create/', NotesCreateView.as_view(), name="note create"),
    path('details/<int:pk>/', NotesDetailView.as_view(), name="note detail"),
    path('update/<int:pk>/', NotesUpdateView.as_view(), name="note update"),
    path('delete/<int:pk>/', NotesDeleteView.as_view(), name="note delete"),
]
