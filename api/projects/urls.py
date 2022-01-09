from rest_framework import routers

from api.projects.viewsets import ProjectViewSet


router = routers.DefaultRouter()
router.register(r"", ProjectViewSet, basename="")
urlpatterns = router.urls
