# Generated by Django 4.0.1 on 2022-04-04 16:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks_management', '0002_alter_task_is_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='image_url',
            field=models.ImageField(blank=True, null=True, upload_to='tasks/'),
        ),
    ]
