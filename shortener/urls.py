from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import (LangingPageView, ShortenedLinkViewSet, UserCabinetView,
                    log_in, log_out, redirect_full_url, signup)

router = DefaultRouter()
router.register(r"shortened-links", ShortenedLinkViewSet, basename="short-links")


api_urlpatterns = [path("", include(router.urls))]


urlpatterns = [
    path("api/", include(api_urlpatterns)),
    re_path(
        r"(?P<shortened_url>[a-zA-z]{8})$", redirect_full_url, name="redirect_full_url"
    ),
    path("", LangingPageView.as_view(), name="landing_page"),
    path("signup/", signup, name="signup"),
    path("login/", log_in, name="login"),
    path("cabinet/", UserCabinetView.as_view(), name="user_cabinet"),
    path("logout/", log_out, name="logout"),
]
