from django.test import TestCase, Client
from django.urls import reverse


class TestNoteList(TestCase):
    def test_about_correct_url(self):
        client = Client()
        response = client.get(reverse('notes list'))
        self.assertEqual(response.status_code, 200)

    def test_about_correct_template(self):
        client = Client()
        response = client.get(reverse('notes list'))
        self.assertTemplateUsed(response, 'notes_list.html')



