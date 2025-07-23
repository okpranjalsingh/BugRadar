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
    reported_by = serializers.ReadOnlyField(source='reported_by.username')
    assigned_to = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all(), allow_null=True, required=False)
    assigned_by = serializers.ReadOnlyField(source='assigned_by.username')
    status = serializers.SlugRelatedField(slug_field='name', queryset=Status.objects.all())
    priority = serializers.SlugRelatedField(slug_field='levels', queryset=Priority.objects.all())
    project = serializers.SlugRelatedField(slug_field='name', queryset=Project.objects.all())

    class Meta:
        model = Bug
        fields = '__all__'
        read_only_fields = ['reported_by', 'assigned_by', 'created_at', 'updated_at']



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

        