from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):

    birth = models.DateField(
        null=True,
        blank=True,
    )

    description = models.TextField(
        null=True,
        blank=True,
    )

    gender = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=(
            ('m', 'Male'),
            ('f', 'Female'),
            ('none', 'Do not show')
        )
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
