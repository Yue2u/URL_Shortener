from django.utils import timezone
from rest_framework import serializers

from link_shortener.settings import MAX_CODE_LENGTH

from .models import ShortenedLink
from .utils import format_url, generate_code


class ResponseShortenedLinkSerializer(serializers.ModelSerializer):
    """Serializer class for ShortenedLink creating
    JSON for response"""

    class Meta:
        model = ShortenedLink
        exclude = ["user"]

    def to_representation(self, data):
        return {
            "id": data.id,
            "full_url": format_url(data.full_url),
            "identifier": data.identifier,
            "last_use": data.last_use,
        }


class ShortenedLinkSerializer(serializers.ModelSerializer):
    """Serializer class for ShortenedLink implementing
    request parsing and new models creating"""

    class Meta:
        model = ShortenedLink
        fields = ["full_url"]

    def create(self, validated_data):
        code = generate_code(MAX_CODE_LENGTH)
        while ShortenedLink.objects.filter(identifier=code).first() is not None:
            code = generate_code(MAX_CODE_LENGTH)

        return ShortenedLink.objects.create(
            full_url=validated_data["full_url"],
            identifier=code,
            last_use=timezone.now(),
            user=self.context["request"].user,
        )

    def to_representation(self, data):
        return ResponseShortenedLinkSerializer(context=self.context).to_representation(
            data
        )
