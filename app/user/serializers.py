from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as translate
from rest_framework import serializers


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["email", "name", "password"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_user_data):
        return get_user_model().objects.create_user(**validated_user_data)


class CreateTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password", "trim_whitespace": False},
    )

    def validate(self, attrs: dict):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )

        if not user:
            msg = translate("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        print(attrs)
        return attrs
