from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notesApp.notes_management.models import Note
from notesApp.tasks_management.models import Task
from tests.core import UserAndClientMixin

ModelUser = get_user_model()


class TaskCreateTests(TestCase, UserAndClientMixin):

    VALID_TASK_CREDENTIALS = {
        'name': 'idk',
        'text': 'random',
    }

    def test_about_correct_url_when_not_authenticated_user_expect_redirect_to_create_profile(self):
        client = Client()
        response = client.get(reverse('task create'))
        self.assertEqual(response.status_code, 302)  # 302 -> should redirect the user to the login page

    def test_about_correct_url_when_authenticated_user_expect_success(self):
        user, client = self.login()  # function to authenticate user ,because the vie has user required !
        response = client.get(reverse('task create'))
        self.assertEqual(response.status_code, 200)

    def test_about_correct_template(self):
        user, client = self.login()
        response = client.get(reverse('task create'))
        self.assertTemplateUsed(response, 'tasks/create_task.html')

    def test_creating_task_with_valid_data_expect_success(self):
        user, client = self.login()

        response = client.post(reverse('task create'), self.VALID_TASK_CREDENTIALS)
        self.assertEqual(Task.objects.count(), 1)  # check if the object is created
        self.assertEqual(response.status_code,
                         302)  # check if the user is redirected to the main page after creating the note
        self.assertRedirects(response,
                             reverse('notes list'))  # double check if you want to redirected to the wanted url

    def test_creating_note_with_invalid_data_expect_failure(self):
        user, client = self.login()

        client.post(reverse('task create'), {
            'text': 'random',
        })
        self.assertEqual(Note.objects.count(), 0)