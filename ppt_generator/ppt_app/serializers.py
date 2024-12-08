# ppt_app/serializers.py
from rest_framework import serializers
from .models import Presentation


class PresentationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presentation
        fields = [
            "id",
            "topic",
            "description",
            "num_slides",
            "theme",
            "create_time",
            "update_time",
            "status",
        ]
        read_only_fields = ["id", "create_time", "update_time", "status"]

    def create(self, validated_data):
        # Manually add the user to the validated_data before saving
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
