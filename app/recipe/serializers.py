"""Serializers for Recipe REST API"""

from core.models import Recipe, Tag
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag views"""

    class Meta:
        model = Tag
        fields = ["name", "id"]
        read_only_fields = ["id"]


class RecipeSerializer(serializers.ModelSerializer):
    """Serializer for recipes"""

    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = ["id", "title", "time_minutes", "price", "link", "tags"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        """Create a recipe with create tags within"""

        tags = validated_data.pop("tags", [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop("tags", None)
        if tags:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        self._set_value_to_instance(instance, validated_data)

        instance.save()
        return instance

    def _get_or_create_tags(self, tags, recipe):
        current_user = self.context["request"].user
        for tag in tags:
            tag_entity, _ = Tag.objects.get_or_create(user=current_user, **tag)
            recipe.tags.add(tag_entity)

    def _set_value_to_instance(self, instance, validate_data):
        for key, value in validate_data.items():
            setattr(instance, key, value)


class RecipeDetailsSerializer(RecipeSerializer):
    """Serializer for recipe detail view"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ["description"]
