from django.urls import path

from notesApp.payment_management.views import charge, success_message

urlpatterns = [
    path('charge/', charge, name='charge'),
    path('sucess/<str:args>/', success_message, name='success message'),
]