from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.projects.models import Project

from api.projects.serializers import ProjectPostSerializer, ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectSerializer
        if self.action == "create":
            return ProjectPostSerializer

    def get_queryset(self):
        queryset = Project.objects.all()

        # Filter by phrase.
        phrase = self.request.GET.get("phrase")
        if phrase is not None:
            for term in phrase.split():
                queryset = queryset.filter(title__icontains=term)

        return queryset
