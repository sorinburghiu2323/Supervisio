import ast

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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

    def create(self, request, *args, **kwargs):
        # Validation checks.
        user = request.user
        if not user.is_supervisor:
            return Response(
                {"detail": "Only a supervisor can create interests."}, status=403
            )
        name = request.data.get("name", None)
        if name is None:
            return Response({"detail": "Required body missing."}, status=400)

        # Get or create the interest.
        # If it exists and it is marked as favourite by the user, return error.
        name = name.lower()
        interest, created = Interest.objects.get_or_create(name=name)
        if not created and interest in user.interests.all():
            return Response(
                {"detail": "Interest is already marked as favourite."}, status=400
            )
        user.interests.add(interest)
        return Response(InterestSerializer(interest).data)

    def patch(self, request, *args, **kwargs):
        # Check body.
        interests = request.data.get("interests", None)
        if interests is None:
            return Response({"detail": "Required body missing."}, status=400)

        # Check if body is in right format.
        try:
            interests = ast.literal_eval(interests)
            interests = Interest.objects.filter(id__in=interests)
        except Exception:
            return Response({"detail": "Invalid body."}, status=400)
        request.user.interests.set(interests)
        return Response(200)
