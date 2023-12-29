import json

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from rest_framework.authtoken.models import Token

from link_shortener.settings import MAX_CODE_LENGTH
from shortener.models import ShortenedLink
from shortener.utils import format_url, generate_code

from .forms import LinkToShortenForm


class LandingPageView(View):
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
    shortened_url = shortened_url.lower()
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
