from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Project,
    Status,
    Priority,
    Bug,
)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields= '__all__'


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields= '__all__'


class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields= '__all__'


class BugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bug
        fields= '__all__'