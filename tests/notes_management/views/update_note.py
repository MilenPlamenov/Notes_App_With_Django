from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from tests.notes_management.views.core import UserAndClientGenerator, create_valid_note

ModelUser = get_user_model()


class NoteUpdateTests(TestCase, UserAndClientGenerator):
    def test_about_correct_url_when_not_authenticated_user_expect_redirect_to_create_profile(self):
        client = Client()
        response = client.get(reverse('note update', args=(3,)))
        self.assertEqual(response.status_code, 302)

    def test_about_correct_url_when_authenticated_user_expect_success(self):
        user, client = self.login()
        note_one = create_valid_note(user)
        response = client.get(reverse('note update', args=(note_one.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_about_correct_template(self):
        user, client = self.login()
        note_one = create_valid_note(user)
        response = client.get(reverse('note update', args=(note_one.id,)))
        self.assertTemplateUsed(response, 'notes/update_notes.html')

    # def test_editing_note_with_valid_data_expect_success(self):
    #     user, client = self.login()
    #     note_one = Note.objects.create(subject='fwq', user_id=user.id)
    #     response = client.get(reverse('note update', args=(note_one.id,)))
    #
    #     self.assertEqual(note_one.subject, 'new subject')

    def test_if_different_user_try_to_edit_other_user_note(self):
        user, client = self.login()  # logged user ,but made the note to refer to user2
        user2 = ModelUser.objects.create_user(username='user2')
        note_one = create_valid_note(user2)
        response = client.get(reverse('note update', args=(note_one.id,)))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('notes list'))
