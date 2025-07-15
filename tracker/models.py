from django.db import models
from django.contrib.auth.models import User
import uuid

class Project(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=50)
    description = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Priority(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    levels = models.CharField(max_length=50, default="Medium")

    def __str__(self):
        return self.levels


class Bug(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=200, null=True, blank=True)
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='bugs')
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name='bugs')
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE, related_name='bugs')

    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_bugs')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_to')
    assigned_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_bugs')  # ✅ NEW FIELD

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
