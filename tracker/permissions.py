from rest_framework import permissions

class IsReporterOrAssigneeOrReadOnly(permissions.BasePermission):

        """
    Custom permission to:
    - Allow GET/HEAD/OPTIONS to all authenticated users
    - Allow PUT/PATCH only to reporter or assigned user
    - Allow DELETE only to reporter
    """
        
        def has_object_permission(self, request, view, obj):
                if request.method in permissions.SAFE_METHODS:
                        return True
                
                #delete only reporter
                if request.method == 'DELETE':
                        return obj.reported_by == request.user
                
                #put/patch = Reporter or Assigned developer
                return (
                        obj.reported_by == request.user or 
                        obj.assigned_by == request.user
                )