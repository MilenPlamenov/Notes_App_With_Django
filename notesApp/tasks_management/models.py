from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    NAME_MAX_LEN = 20

    name = models.CharField(
        max_length=NAME_MAX_LEN,
    )

    text = models.TextField(
        blank=True,
        null=True,
    )

    is_done = models.BooleanField(
        default=False,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
