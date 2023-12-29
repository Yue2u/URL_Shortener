from drf_spectacular.utils import extend_schema, extend_schema_view
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from .models import ShortenedLink
from .serializers import (ResponseShortenedLinkSerializer,
                          ShortenedLinkSerializer)


@extend_schema_view(
    list=extend_schema(
        summary="Get list of shortened links for authentificated user",
        responses={status.HTTP_200_OK: ResponseShortenedLinkSerializer},
    ),
    create=extend_schema(
        summary="Create new shortened link for authentificated user",
        responses={status.HTTP_200_OK: ResponseShortenedLinkSerializer},
    ),
    retrieve=extend_schema(
        summary="Get shortened link by id for authentificated user",
        responses={status.HTTP_200_OK: ResponseShortenedLinkSerializer},
    ),
    destroy=extend_schema(
        summary="Delete shortened link id pk for authentificated user",
        responses={status.HTTP_200_OK: ResponseShortenedLinkSerializer},
    ),
)
class ShortenedLinkViewSet(viewsets.ModelViewSet):
    """API endpoint that handles ShortenedLinks model"""

    serializer_class = ShortenedLinkSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):
        return ShortenedLink.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        for entity in queryset:
            entity.update_last_use()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.update_last_use()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ShortenedLinkByCode(APIView):
    """API endpoint that handles ShortenedLinks model,
    return ShortenedLinks instance by shortened url code"""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    @extend_schema(summary="Get shortened link by code for authentificated user",
                   responses={status.HTTP_200_OK: ResponseShortenedLinkSerializer})
    def get(self, request, shortened_url_code):
        shortened_url_code = shortened_url_code.lower()
        instance = get_object_or_404(ShortenedLink, user=request.user, identifier=shortened_url_code)
        instance.update_last_use()
        serializer = ShortenedLinkSerializer(instance)
        return Response(serializer.data)
