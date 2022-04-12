from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notesApp.notes_management.models import Note

ModelUser = get_user_model()


class NoteCreateTests(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'test1',
        'password': '12345qwe',
    }
    VALID_PROFILE_CREDENTIALS = {
        'gender': 'm',
    }

    VALID_NOTE_CREDENTIALS = {
        'subject': 'idk',
        'text': 'random',
        'date': '2022-04-09 19:37:09',
    }

    def login(self):
        self.username = self.VALID_USER_CREDENTIALS['username']
        self.password = self.VALID_USER_CREDENTIALS['password']
        user = ModelUser.objects.create_user(username=self.username)
        user.set_password(self.password)
        user.save()
        client = Client()
        client.login(username=self.username, password=self.password)
        return user, client

    def test_about_correct_url_when_not_authenticated_user_expect_redirect_to_create_profile(self):
        client = Client()
        response = client.get(reverse('note create'))
        self.assertEqual(response.status_code, 302)  # 302 -> should redirect the user to the login page

    def test_about_correct_url_when_authenticated_user_expect_success(self):
        user, client = self.login()  # function to authenticate user ,because the vie has user required !
        response = client.get(reverse('note create'))
        self.assertEqual(response.status_code, 200)

    def test_about_correct_template(self):
        user, client = self.login()
        response = client.get(reverse('note create'))
        self.assertTemplateUsed(response, 'notes/create.html')

    def test_creating_note_with_valid_data_expect_success(self):
        user, client = self.login()

        response = client.post(reverse('note create'), self.VALID_NOTE_CREDENTIALS)
        self.assertEqual(Note.objects.count(), 1)  # check if the object is created
        self.assertEqual(response.status_code,
                         302)  # check if the user is redirected to the main page after creating the note
        self.assertRedirects(response,
                             reverse('notes list'))  # double check if you want to redirected to the wanted url

    def test_creating_note_with_invalid_data_expect_failure(self):
        user, client = self.login()

        response = client.post(reverse('note create'), {
            'text': 'random',
            'date': 'invalid date',
        })
        self.assertEqual(Note.objects.count(), 0)