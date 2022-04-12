from django.contrib.auth import get_user_model
from django.test import Client


class LoginFunction:
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
