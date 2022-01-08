from rest_framework import serializers

from api.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "is_supervisor",
            "capacity",
            "bio",
        ]


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "capacity",
            "bio",
        ]

    def update(self, instance, validated_data):
        instance.capacity = validated_data.get("capacity", instance.capacity)
        instance.bio = validated_data.get("bio", instance.bio)
        return super().update(instance, validated_data)
