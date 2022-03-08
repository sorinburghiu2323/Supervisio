from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.grades.models import Grade, Module
from rest_framework.response import Response
from rest_framework.decorators import action

from api.grades.serializers import ModuleSerializer


class ModuleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return ModuleSerializer

    def get_queryset(self):
        queryset = Module.objects.all()
        return queryset

    def destroy(self, request, *args, **kwargs):
        user = request.user
        if user.is_supervisor:
            return Response({"detail": "Only students can delete grades."}, status=403)

        # Check if grade exists, delete it if it does.
        grade = Grade.objects.filter(student=user, module=self.get_object())
        if grade:
            grade.delete()
            return Response(status=200)
        return Response({"detail": "No grade for this module."}, status=400)

    @action(
        detail=True,
        methods=["POST"],
        url_path="",
        authentication_classes=[IsAuthenticated],
    )
    def create_grade(self, request, pk):
        user = request.user
        if user.is_supervisor:
            return Response({"detail": "Only students can delete grades."}, status=403)
        score = request.data.get("score")
        if score is None or 0 > score > 100:
            return Response({"detail": "Wrong body."}, status=400)

        # Update or create grade with score.
        Grade.objects.update_or_create(
            user=user, module=self.get_object(), defaults={"score": score}
        )
        return Response(status=200)
