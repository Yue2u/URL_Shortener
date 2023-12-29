from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import ShortenedLinkByCode, ShortenedLinkViewSet

router = DefaultRouter()
router.register(r"shortened-links", ShortenedLinkViewSet, basename="short-links")


urlpatterns = [
    path("api/", include(router.urls)),
    re_path(
        r"^api/shortened-links/(?P<shortened_url_code>[a-zA-z]{8})$",
        ShortenedLinkByCode.as_view(),
    ),
]
