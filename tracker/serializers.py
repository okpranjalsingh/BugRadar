from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Project,
    Status,
    Priority,
    Bug,
    BugComment,
    BugAttachment
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



class BugCommentSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = BugComment
        fields = ['id', 'bug', 'author', 'author_name', 'content', 'created_at']
        read_only_fields = ['author', 'created_at']


class BugAttachmentSerializer(serializers.ModelSerializer):
    uploded_by = serializers.StringRelatedField(read_only = True)

    class Meta:
        model = BugAttachment
        fields = '__all__'