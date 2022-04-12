from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notesApp.notes_management.models import Note
from tests.notes_management.views.core import UserAndClientGenerator, create_valid_note

ModelUser = get_user_model()


class NoteDeleteTests(TestCase, UserAndClientGenerator):
    def test_about_correct_url_when_not_authenticated_user_expect_redirect_to_create_profile(self):
        client = Client()
        response = client.get(reverse('note delete', args=(3,)))
        self.assertEqual(response.status_code, 302)

    def test_about_correct_url_when_authenticated_user_expect_success(self):
        user, client = self.login()
        note_one = create_valid_note(user)
        response = client.get(reverse('note delete', args=(note_one.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_about_correct_template(self):
        user, client = self.login()
        note_one = create_valid_note(user)
        response = client.get(reverse('note delete', args=(note_one.id,)))
        self.assertTemplateUsed(response, 'notes/delete_notes.html')
