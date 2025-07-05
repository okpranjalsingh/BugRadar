from django.db import models

# Create your models here

import uuid

class Project(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable= False, unique= True)
    name = models.CharField(max_length=50)
    description = models.CharField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,unique=True, editable=False)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Priority(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,unique=True, editable=False)
    levels = models.CharField(max_length=50, default="Medium")

    def __str__(self):
        return self.level
    