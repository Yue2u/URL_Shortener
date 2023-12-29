from django.urls import path, re_path

from .views import (LandingPageView, UserCabinetView, log_in, log_out,
                    redirect_full_url, signup)

urlpatterns = [
    re_path(
        r"^(?P<shortened_url>[a-zA-z]{8})$", redirect_full_url, name="redirect_full_url"
    ),
    path("", LandingPageView.as_view(), name="landing_page"),
    path("signup/", signup, name="signup"),
    path("login/", log_in, name="login"),
    path("cabinet/", UserCabinetView.as_view(), name="user_cabinet"),
    path("logout/", log_out, name="logout"),
]
