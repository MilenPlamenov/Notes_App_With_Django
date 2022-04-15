from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notesApp.tasks_management.models import Task
from tests.core import UserAndClientMixin, create_valid_task

ModelUser = get_user_model()


class TaskDeleteTests(TestCase, UserAndClientMixin):
    def test_about_correct_url_when_not_authenticated_user_expect_redirect_to_create_profile(self):
        client = Client()
        response = client.get(reverse('task delete', args=(3,)))
        self.assertEqual(response.status_code, 302)

    def test_about_correct_url_when_authenticated_user_expect_success(self):
        user, client = self.login()
        task_one = create_valid_task(user)
        response = client.get(reverse('task delete', args=(task_one.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_about_correct_template(self):
        user, client = self.login()
        task_one = create_valid_task(user)
        response = client.get(reverse('task delete', args=(task_one.id,)))
        self.assertTemplateUsed(response, 'tasks/delete_task.html')

    def test_if_the_logic_of_the_view_works_correctly(self):
        user, client = self.login()

        task_one = create_valid_task(user)
        self.assertEqual(Task.objects.count(), 1)
        response = client.post(reverse('task delete', args=(task_one.id,)))
        self.assertEqual(Task.objects.count(), 0)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes list'))

    def test_if_different_user_try_to_delete_other_user_task(self):
        user, client = self.login()  # logged user ,but made the note to refer to user2
        user2 = ModelUser.objects.create_user(username='user2')
        task_one = create_valid_task(user2)
        response = client.get(reverse('task delete', args=(task_one.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes list'))