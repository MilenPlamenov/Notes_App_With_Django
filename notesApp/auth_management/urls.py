from django.contrib.auth.views import LogoutView
from django.urls import path

from notesApp.auth_management.views import create_profile, edit_profile, login_view, change_password, delete_profile

urlpatterns = [
    path('profile/create/', create_profile, name="create profile"),
    path('profile/edit/', edit_profile, name="edit profile"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('login/', login_view, name="login"),
    path('changepass/', change_password, name="change password"),
    path('profile/delete/<int:pk>/', delete_profile, name="delete profile"),
]