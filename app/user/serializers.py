from django.contrib.auth import get_user_model
from rest_framework import serializers


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "name", "password"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_user_data):
        return get_user_model().objects.create_user(**validated_user_data)
