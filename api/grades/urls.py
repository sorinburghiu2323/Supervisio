from rest_framework import routers

from api.grades.viewsets import ModuleViewSet


router = routers.DefaultRouter()
router.register(r"modules", ModuleViewSet, basename="modules")
urlpatterns = router.urls
