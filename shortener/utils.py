import random
import string
from urllib.parse import urlparse


def generate_code(code_length):
    letters = string.ascii_lowercase
    code = [letters[random.randint(0, len(letters) - 1)] for _ in range(code_length)]
    return "".join(code)


def format_url(url):
    parsed = urlparse(url, scheme="http")
    if not parsed.netloc:
        parsed = parsed._replace(netloc=parsed.path.lstrip("/"))
        parsed = parsed._replace(path="")
    netloc = (
        "www." + parsed.netloc
        if not parsed.netloc.startswith("www.")
        else parsed.netloc
    )
    parsed = parsed._replace(netloc=netloc)
    return parsed.geturl()
