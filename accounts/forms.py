from django import forms
from django.core.validators import URLValidator


class LinkToShortenForm(forms.Form):
    full_url = forms.CharField(
        label="Insert link here",
        max_length=150,
        required=True,
        validators=[URLValidator],
    )
    shortened_url = forms.CharField(label="Generated link", required=False)
