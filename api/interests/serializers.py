from rest_framework import serializers

from api.interests.models import Interest


class InterestSerializer(serializers.ModelSerializer):
    is_favourite = serializers.SerializerMethodField()

    class Meta:
        model = Interest
        fields = [
            "id",
            "name",
            "is_favourite",
        ]

    def get_is_favourite(self, obj):
        request = self.context.get("request", None)
        return request and obj in request.user.interests.all()
