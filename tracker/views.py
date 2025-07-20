from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from .permissions import IsReporterOrAssigneeOrReadOnly
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models  
from rest_framework.decorators import action
from rest_framework.response import Response



from .models import (
    Project,
    Status,
    Priority,   
    Bug,
    BugComment,
    BugAttachment
    
)
from .serializers import (
    PrioritySerializer,
    StatusSerializer,
    ProjectSerializer,
    BugSerializer,
    BugCommentSerializer,
    BugAttachmentSerializer
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
    permission_classes = [IsAuthenticated, IsReporterOrAssigneeOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority', 'assigned_to'] 

    def get_queryset(self):  
        user = self.request.user
        if user.is_superuser:
            return Bug.objects.all()
        return Bug.objects.filter(models.Q(assigned_to=user) | models.Q(reported_by=user))

    def perform_update(self, serializer):
        bug = self.get_object()
        user = self.request.user
        old_status = bug.status.name

        new_status_obj = serializer.validated_data.get('status')
        new_assigned_to = serializer.validated_data.get('assigned_to', None)

        # Validate status transition if status is being changed
        if new_status_obj:
            new_status = new_status_obj.name
            valid_transitions = {
                "Open": ["In Progress"],
                "In Progress": ["Resolved"],
                "Resolved": ["Closed", "Reopened"],
                "Closed": ["Open"],
            }
            allowed_next = valid_transitions.get(old_status, [])
            if new_status not in allowed_next:
                raise PermissionDenied(f"Invalid status transition: {old_status} ➝ {new_status}")

        # Only reporter or assignee can update the bug
        if user != bug.reported_by and user != bug.assigned_to:
            raise PermissionDenied("You are not allowed to change this bug.")

        # Update assigned_by if assignment changes
        if new_assigned_to and bug.assigned_to != new_assigned_to:
            serializer.save(assigned_by=user)
        else:
            serializer.save()

# bug assigned to developer
class MyBugViewSet(viewsets.ReadOnlyModelViewSet):
    '''
      shows only bug assigned to logged-in users only.
    '''
    serializer_class = BugSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'priority', 'assigned_to']

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Bug.objects.all() 
        return Bug.objects.filter(models.Q(assigned_to=user) | models.Q(reported_by=user))
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        queryset = self.get_queryset()  

        total = queryset.count()
        open_count = queryset.filter(status__name="Open").count()
        in_progress_count = queryset.filter(status__name="In Progress").count()
        resolved_count = queryset.filter(status__name="Resolved").count()
        closed_count = queryset.filter(status__name="Closed").count()

        data = {
            "total": total,
            "open": open_count,
            "in_progress": in_progress_count,
            "resolved": resolved_count,
            "closed": closed_count
        }

        return Response(data)


class BugCommentViewset(viewsets.ModelViewSet):
    queryset = BugComment.objects.all()
    serializer_class = BugCommentSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class BugAttachmentViewSet(viewsets.ModelViewSet):
    queryset = BugAttachment.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BugAttachmentSerializer

    def perform_create(self, serializer):
        serializer.save(uploded_by = self.request.user)
        
