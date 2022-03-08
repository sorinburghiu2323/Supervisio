from rest_framework import serializers

from api.grades.models import Grade, Module


class ModuleSerializer(serializers.ModelSerializer):
    score = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = [
            "id",
            "name",
            "code",
            "score",
        ]

    def get_score(self, obj):
        request = self.context.get("request", None)
        if request:
            grade = Grade.objects.filter(student=request.user, module=obj)
            if grade:
                return grade.score
