import string
from random import SystemRandom
from django.utils.text import slugify


def random_letters(size=4):
    return ''.join(SystemRandom().choices(
        string.ascii_lowercase + string.digits,
        k=size
    ))


def slugify_new(text, size=4):
    return slugify(text) + '-' + random_letters(size)
