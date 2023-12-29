import json

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from link_shortener.settings import MAX_CODE_LENGTH

from .forms import LinkToShortenForm
from .models import ShortenedLink
from .serializers import (ResponseShortenedLinkSerializer,
                          ShortenedLinkSerializer)
from .utils import format_url, generate_code


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


class LangingPageView(View):
    def get(self, request):
        return render(
            request, "landing_page.html", context={"form": LinkToShortenForm()}
        )

    def post(self, request):
        form = LinkToShortenForm(request.POST)

        if form.is_valid():
            user = (
                request.user
                if request.user.is_authenticated
                else User.objects.get(username="guest")
            )
            full_url = form.cleaned_data["full_url"]

            code = generate_code(MAX_CODE_LENGTH)
            while ShortenedLink.objects.filter(identifier=code).first() is not None:
                code = generate_code(MAX_CODE_LENGTH)

            response_form = LinkToShortenForm(
                initial={
                    "full_url": full_url,
                    "shortened_url": request.META["HTTP_HOST"] + "/" + code,
                }
            )

            ShortenedLink.objects.create(full_url=full_url, identifier=code, user=user)

            return render(request, "landing_page.html", context={"form": response_form})

        return render(
            request, "landing_page.html", context={"form": LinkToShortenForm()}
        )


class UserCabinetView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            redirect("landing_page", context={"form": LinkToShortenForm()})
        user_urls = ShortenedLink.objects.filter(user=request.user)
        items = []

        for item in user_urls:
            items.append(
                (item.full_url, request.META["HTTP_HOST"] + "/" + item.identifier)
            )
            item.update_last_use()

        token = Token.objects.get(user=request.user)
        return render(
            request,
            "cabinet.html",
            context={"shortened_urls": items, "token": "Token " + str(token)},
        )

    def post(self, request):
        json_ = json.loads(request.body.decode("utf-8"))
        identifier = json_["shortened_url"].split("/")[1]
        get_object_or_404(ShortenedLink, identifier=identifier).delete()
        return redirect("user_cabinet")


def redirect_full_url(request, shortened_url):
    shortend_url = get_object_or_404(ShortenedLink, identifier=shortened_url)
    shortend_url.update_last_use()
    print(format_url(shortend_url.full_url))
    return redirect(format_url(shortend_url.full_url))


def landing_page(request):
    return render(request, "landing_page.html")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "signup.html", {"form": form})


def log_in(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("user_cabinet")
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


def log_out(request):
    logout(request)
    return redirect("landing_page")
