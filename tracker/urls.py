from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    StatusViewSet,
    PriorityViewSet,
    BugViewSet,
    MyBugViewSet
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'statuses', StatusViewSet)
router.register(r'priorities', PriorityViewSet)
router.register(r'bugs', BugViewSet)
router.register(r'my-bugs', MyBugViewSet, basename='my-bugs' )


urlpatterns =[
    path('', include(router.urls))
]