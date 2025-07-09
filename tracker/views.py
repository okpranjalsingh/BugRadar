from django.shortcuts import render
from rest_framework import viewsets
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

class StatusViewSet(viewsets.ModelViewset):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class PriorityViewSets(viewsets.ModelViewSet):
    queryset = Priority.objects.all()
    serializer_class = PrioritySerializer

class BugViewSets(viewsets.ModelViewSet):
    queryset = Bug.objects.all()
    serializer_class = BugSerializer