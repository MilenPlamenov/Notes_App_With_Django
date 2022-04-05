from django.contrib.auth.views import LogoutView
from django.urls import path

from notesApp.auth_management.views import create_profile, edit_profile, login_view, change_password, delete_profile, \
    ProfileDetailView, profile_details

urlpatterns = [
    path('profile/create/', create_profile, name="create profile"),
    path('profile/edit/', edit_profile, name="edit profile"),
    path('profile/details/<int:pk>/', profile_details, name="details profile"),
    path('profile/delete/<int:pk>/', delete_profile, name="delete profile"),
    path('login/', login_view, name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('changepass/', change_password, name="change password"),
]