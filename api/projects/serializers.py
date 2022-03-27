from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from api.interests.serializers import InterestSerializer

from api.projects.models import Project, ProjectApplication
from api.users.serializers import UserSerializer


class ProjectSerializer(serializers.ModelSerializer):
    supervisor = UserSerializer()
    applications_count = serializers.SerializerMethodField()
    application_sent = serializers.SerializerMethodField()
    interests = InterestSerializer(many=True)

    class Meta:
        model = Project
        fields = [
            "id",
            "supervisor",
            "title",
            "description",
            "views",
            "applications_count",
            "application_sent",
            "interests",
        ]

    def get_applications_count(self, obj):
        return ProjectApplication.objects.filter(project=obj).count()

    def get_application_sent(self, obj):
        request = self.context.get("request", None)
        return (
            request
            and ProjectApplication.objects.filter(
                student=request.user, project=obj
            ).exists()
        )


class ProjectPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "title",
            "description",
            "interests",
        ]

    def create(self, validated_data):
        request = self.context.get("request", None)
        if not request or not request.user.is_supervisor:
            return ValidationError({"detail": "Only supervisors can create projects."})
        validated_data["supervisor"] = request.user
        return super().create(validated_data)


class ProjectApplicationSerializer(serializers.ModelSerializer):
    student = UserSerializer()
    project = ProjectSerializer()

    class Meta:
        model = ProjectApplication
        fields = [
            "id",
            "student",
            "project",
            "message",
            "status",
        ]
