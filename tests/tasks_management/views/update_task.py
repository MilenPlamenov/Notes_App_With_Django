from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notesApp.tasks_management.models import Task
from tests.core import UserAndClientMixin, create_valid_task

ModelUser = get_user_model()


class TestTaskUpdate(TestCase, UserAndClientMixin):
    def test_about_correct_url_when_not_authenticated_user_expect_redirect_to_login_page(self):
        client = Client()
        response = client.get(reverse('task update', args=(3,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_about_correct_url_when_authenticated_user_expect_success(self):
        user, client = self.login()
        task_one = create_valid_task(user)
        response = client.get(reverse('task update', args=(task_one.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_about_correct_template(self):
        user, client = self.login()
        task_one = create_valid_task(user)
        response = client.get(reverse('task update', args=(task_one.id,)))
        self.assertTemplateUsed(response, 'tasks/edit_task.html')

    def test_editing_task_with_valid_data_expect_success(self):
        user, client = self.login()
        task_one = create_valid_task(user)
        response = client.post(reverse('task update', args=(task_one.id,)), data={'name': 'changed name'})

        updated_task = Task.objects.get(pk=task_one.pk)
        self.assertEqual(updated_task.name, 'changed name')
        self.assertRedirects(response, reverse('notes list'))

    def test_if_different_user_try_to_edit_other_user_task(self):
        user, client = self.login()  # logged user ,but made the note to refer to user2
        user2 = ModelUser.objects.create_user(username='user2')
        task_one = create_valid_task(user2)
        response = client.get(reverse('task update', args=(task_one.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes list'))
