from django.contrib.auth.views import LogoutView
from django.urls import path

from notesApp.notes_management.views import notes_list, create_note, NotesDetailView, update_note, \
    NotesDeleteView, create_profile, login_view, delete_note, edit_profile, change_password, delete_profile

urlpatterns = [
    path('', notes_list, name="notes list"),
    path('create/', create_note, name="note create"),
    path('details/<int:pk>/', NotesDetailView.as_view(), name="note detail"),
    path('update/<int:pk>/', update_note, name="note update"),
    path('delete/<int:pk>/', delete_note, name="note delete"),
    path('profile/create/', create_profile, name="create profile"),
    path('profile/edit/<int:pk>/', edit_profile, name="edit profile"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('login/', login_view, name="login"),
    path('changepass/', change_password, name="change password"),
    path('profile/delete/<int:pk>/', delete_profile, name="delete profile"),
]
