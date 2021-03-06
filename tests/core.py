from django.contrib.auth import get_user_model
from django.test import Client

from notesApp.notes_management.models import Note
from notesApp.tasks_management.models import Task


def create_valid_note(user):
    note = Note.objects.create(subject='fwq', text='random', date='2022-04-09 19:37:09', user_id=user.id)
    return note


def create_valid_task(user):
    note = Task.objects.create(name='fwq', text='random', user_id=user.id)
    return note


class UserAndClientMixin:
    ModelUser = get_user_model()
    VALID_USER_CREDENTIALS = {
        'username': 'test1',
        'password': '12345qwe',
    }

    def login(self):
        self.username = self.VALID_USER_CREDENTIALS['username']
        self.password = self.VALID_USER_CREDENTIALS['password']
        user = self.ModelUser.objects.create_user(username=self.username)
        user.set_password(self.password)
        user.save()
        client = Client()
        client.login(username=self.username, password=self.password)
        return user, client
