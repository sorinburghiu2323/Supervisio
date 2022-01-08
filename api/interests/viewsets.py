from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.interests.models import Interest

from api.interests.serializers import InterestSerializer
from api.utils import convert_to_bool


class InterestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return InterestSerializer

    def get_queryset(self):
        queryset = Interest.objects.all()

        # Filter by favourite.
        is_favourite = self.request.GET.get("is_favourite")
        if is_favourite is not None:
            interests = self.request.user.interests.all()
            queryset = (
                interests
                if convert_to_bool(is_favourite)
                else queryset.difference(interests)
            )

        return queryset
