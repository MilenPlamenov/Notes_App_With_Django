from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Note(models.Model):
    SUBJECT_MAX_LEN = 20

    IMAGE_UPLOAD_URL = 'notes/'
    subject = models.CharField(
        max_length=SUBJECT_MAX_LEN,
    )

    text = models.TextField(
        blank=True,
        null=True,
    )
    date = models.DateTimeField(
        default=datetime.now,
        blank=True,
        null=True,
    )

    image_url = models.ImageField(
        upload_to=IMAGE_UPLOAD_URL,
        blank=True,
        null=True,
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.subject
