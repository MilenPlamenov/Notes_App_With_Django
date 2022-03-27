from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notesApp.auth_management.models import Profile

ModelUser = get_user_model()


class CreateProfileTest(TestCase):
    VALID_USER_CREDENTIALS = {
        'username': 'test',
        'password': '12345qwe',
    }
    VALID_PROFILE_CREDENTIALS = {
        'gender': 'm',
    }

    def test_about_correct_template(self):
        user = ModelUser.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_CREDENTIALS, user=user)
        self.client.get(reverse('create profile'), kwargs={'pk': profile.pk})
        self.assertTemplateUsed('create_profile.html')

    def test_valid_forms_expect_success(self):
        user = ModelUser.objects.create_user(**self.VALID_USER_CREDENTIALS)
        profile = Profile.objects.create(**self.VALID_PROFILE_CREDENTIALS, user=user)

        response = self.client.post(reverse('create profile'), data={
            user: user,
            profile: profile,
        })
        self.assertEqual(response.status_code, 200)

        users = get_user_model().objects.all()
        profiles = Profile.objects.all()
        self.assertEqual(users.count(), 1)
        self.assertEqual(profiles.count(), 1)
