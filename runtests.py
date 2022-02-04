#!/usr/bin/env python
import sys

from django.conf import settings
from django.core.management import execute_from_command_line

if not settings.configured:
    settings.configure(
        SECRET_KEY="secret key",
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            }
        },
        INSTALLED_APPS=[
            "django.contrib.auth",
            "django.contrib.sessions",
            "django.contrib.contenttypes",
            "vote",
            "test",
        ],
        ROOT_URLCONF="test.urls",
        MIDDLEWARE_CLASSES=[  # Deprecated in Django 1.10 https://docs.djangoproject.com/en/1.11/ref/settings/#middleware-classes
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
        ],
        MIDDLEWARE=[
            "django.contrib.sessions.middleware.SessionMiddleware",
            "django.contrib.auth.middleware.AuthenticationMiddleware",
        ],
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
                "OPTIONS": {
                    "context_processors": [
                        "django.template.context_processors.request",
                        "django.contrib.auth.context_processors.auth",
                    ],
                },
            },
        ],
    )


def runtests():
    argv = sys.argv[:1] + ["test"] + sys.argv[1:]
    execute_from_command_line(argv)


if __name__ == "__main__":
    runtests()
