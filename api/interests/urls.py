from rest_framework import routers

from api.interests.viewsets import InterestViewSet


router = routers.DefaultRouter()
router.register(r"", InterestViewSet, basename="")
urlpatterns = router.urls
