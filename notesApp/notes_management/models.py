from datetime import datetime

from django.db import models


class Note(models.Model):
    subject = models.CharField(max_length=20)
    text = models.TextField(blank=True)
    date = models.DateTimeField(default=datetime.now, blank=True)