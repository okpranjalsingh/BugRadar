# Generated by Django 5.2.1 on 2025-07-17 13:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_bugcomment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BugAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='bug_attachments/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('bug', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='tracker.bug')),
                ('uploded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
