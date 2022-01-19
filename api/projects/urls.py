from rest_framework import routers

from api.projects.viewsets import ProjectApplicationViewSet, ProjectViewSet


router = routers.DefaultRouter()
router.register(r"applications", ProjectApplicationViewSet, basename="applications")
router.register(r"", ProjectViewSet, basename="projects")
urlpatterns = router.urls
