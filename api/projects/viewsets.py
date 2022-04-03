import ast
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from api.projects.models import Project, ProjectApplication
from api.projects.serializers import (
    ProjectApplicationSerializer,
    ProjectPostSerializer,
    ProjectSerializer,
)
from api.recommender.recommender_engine import LinearRecommender
from api.users.serializers import UserSerializer
from api.utils import convert_to_bool


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

        # Filter by interests.
        interests = self.request.GET.get("interests")
        if interests is not None:
            try:
                interests = ast.literal_eval(interests)
                queryset = queryset.filter(interests__in=interests)
            except Exception:
                pass

        # Filter by supervisor.
        supervisor = self.request.GET.get("supervisor")
        if supervisor is not None:
            try:
                queryset = queryset.filter(supervisor=supervisor)
            except Exception:
                pass

        return queryset

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve individual project.
        """
        project = self.get_object()
        project.views += 1
        project.save()
        return Response(
            ProjectSerializer(project, context={"request": request}).data, status=200
        )

    def destroy(self, request, *args, **kwargs):
        """
        Allow a supervisor to delete one of their projects assuming it has
        no active applications.
        """
        project = self.get_object()
        if project.supervisor != request.user:
            return Response(
                {"detail": "Not authorized to delete this project."}, status=403
            )
        if ProjectApplication.objects.filter(
            project=project, status__in=["pending", "approved"]
        ).exists():
            return Response(
                {
                    "detail": "Cannot delete a project that has pending or approved applications."
                },
                status=400,
            )
        project.delete()
        return Response(status=200)

    @action(detail=True, methods=["POST"], url_path="apply")
    def apply_to_project(self, request, pk):
        """
        Students can apply for projects if there is not already an open application for it.
        """
        user = request.user
        if user.is_supervisor:
            return Response(
                {"detail": "Only students can apply for projects."}, status=403
            )
        project = self.get_object()
        applications = ProjectApplication.objects.filter(student=user)
        if applications.filter(
            project=project, status__in=["pending", "approved"]
        ).exists():
            return Response(
                {
                    "detail": "There already exists an open application for this project."
                },
                status=400,
            )
        if applications.filter(status="pending").count() >= 3:
            return Response(
                {"detail": "You cannot have more than 3 open applications at a time."},
                status=400,
            )

        message = request.data.get("message")
        ProjectApplication.objects.create(
            student=user,
            project=project,
            message=message,
        )
        return Response(status=201)

    @action(detail=False, methods=["GET"], url_path="recommendations")
    def get_recommendations(self, request):
        recommender_engine = LinearRecommender(request.user)
        return Response(
            {
                "projects": ProjectSerializer(
                    recommender_engine.get_project_recommendations(), many=True
                ).data,
                "supervisors": UserSerializer(
                    recommender_engine.get_supervisor_recommendations(), many=True
                ).data,
            },
            status=200,
        )


class ProjectApplicationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if not self.request.user.is_supervisor:
            raise PermissionDenied(
                {"detail": "Only supervisors can manage applications."}
            )
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ProjectApplicationSerializer

    def get_queryset(self):
        queryset = ProjectApplication.objects.filter(
            project__supervisor=self.request.user
        )

        # Filter by approved.
        is_approved = self.request.GET.get("is_approved")
        if is_approved is not None:
            queryset = (
                queryset.filter(status="approved")
                if convert_to_bool(is_approved)
                else queryset.filter(status="pending")
            )

        return queryset

    @action(detail=True, methods=["POST"], url_path="review")
    def review_application(self, request, pk):
        """
        Supervisors can review applications for their projects to either approve
        or reject them.
        """
        is_approved = request.data.get("is_approved")
        if is_approved is None:
            return Response({"detail": "Missing required body."}, status=400)
        application = self.get_object()
        application.status = "approved" if convert_to_bool(is_approved) else "rejected"
        application.save()
        return Response(status=200)
