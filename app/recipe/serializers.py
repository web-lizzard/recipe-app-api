"""Serializers for Recipe REST API"""

from core.models import Recipe
from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""

    class Meta:
        model = Recipe
        fields = ["title", "time_minutes", "price", "description", "link"]
        read_only_fields = ["id"]
