from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from notesApp.notes_management.models import Note
from tests.core import UserAndClientMixin, create_valid_note

ModelUser = get_user_model()


class TestNoteDelete(TestCase, UserAndClientMixin):
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

    def test_if_the_logic_of_the_view_works_correctly(self):
        """
            Creating note ->
             test if its created ->
              delete it ->
               test if its deleted ->
                test if redirected to the main page
        """
        user, client = self.login()
        note_one = create_valid_note(user)
        self.assertEqual(Note.objects.count(), 1)
        response = client.post(reverse('note delete', args=(note_one.id,)))
        self.assertEqual(Note.objects.count(), 0)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes list'))
