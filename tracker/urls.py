from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    StatusViewSet,
    PriorityViewSet,
    BugViewSet
)

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'statuses', StatusViewSet)
router.register(r'priorities', PriorityViewSet)
router.register(r'bugs', BugViewSet)


urlpatterns =[
    path("api/", include(router.urls))
]