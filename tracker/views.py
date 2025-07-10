from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import (
    Project,
    Status,
    Priority,
    Bug,
)
from .serializers import (
    PrioritySerializer,
    StatusSerializer,
    ProjectSerializer,
    BugSerializer
)


# Create your views here.

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class PriorityViewSet(viewsets.ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer

class BugViewSet(viewsets.ModelViewSet):
    queryset = Bug.objects.all()
    serializer_class = BugSerializer



# bug assigned to developer

class MyBugViewSet(viewsets.ReadOnlyModelViewSet):
    '''
    shows only bug assigned to logged-in users only.
    '''
    serializer_class = BugSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bug.objects.filter(assigned_to=self.request.user)