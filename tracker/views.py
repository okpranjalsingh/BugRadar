from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from .permissions import IsReporterOrAssigneeOrReadOnly
from rest_framework.exceptions import PermissionDenied



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
    permission_classes = [permissions.IsAuthenticated, IsReporterOrAssigneeOrReadOnly]
    
    
    def perform_update(self, serializer):
        # 1. Get the current instance of the bug (existing bug)
        bug = self.get_object()
        old_status = bug.status.name  # e.g., "Open"

        # 2. Get the new status coming from the update request
        new_status_obj = serializer.validated_data.get('status')
        if not new_status_obj:
            # If status is not being changed, allow update
            serializer.save()
            return
        
        new_status = new_status_obj.name  # e.g., "Resolved"
        
        # 3. Define allowed transitions
        valid_transitions = {
            "Open": ["In Progress"],
            "In Progress": ["Resolved"],
            "Resolved": ["Closed", "Reopened"],
            "Closed": ["Open"],
        }

        # 4. Check if this is a valid transition
        allowed_next = valid_transitions.get(old_status, [])
        if new_status not in allowed_next:
            raise PermissionDenied(f"❌ Invalid status transition: {old_status} ➝ {new_status}")

        # 5. Check who is trying to update
        user = self.request.user

        # 6. Only reporter or assigned dev can do this
        if user != bug.reported_by and user != bug.assigned_to:
            raise PermissionDenied("❌ You are not allowed to change the status of this bug.")

        # 7. All checks passed – Save the update
        serializer.save()



# bug assigned to developer

class MyBugViewSet(viewsets.ReadOnlyModelViewSet):
    '''
      shows only bug assigned to logged-in users only.
    '''
    serializer_class = BugSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Bug.objects.filter(assigned_to=self.request.user)