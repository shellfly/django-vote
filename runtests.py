#!/usr/bin/env python
import sys

from django.conf import settings
from django.core.management import execute_from_command_line
from django.utils.functional import empty


def configure(**options):
    if settings._wrapped is not empty:
        settings._wrapped = empty
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
        **options
    )

if not settings.configured:
    configure()


def runtests():
    argv = sys.argv[:1] + ["test"] + sys.argv[1:]
    execute_from_command_line(argv)
    # Now repeat all the tests when the Vote model has been swappwed with a
    # custom model. Update settings for this.
    configure(VOTE_VOTE_MODEL='test.MyVote')
    from test.models import Comment, MyVote
    from vote.models import VotableManager
    from vote.utils import _reset_vote_model
    # The VoteModel's votes manager has to be updated for the new Vote model
    Comment.votes = VotableManager(MyVote)
    # This is necessary only for tests to clear the previously cached
    # Vote model class.
    _reset_vote_model()
    execute_from_command_line(argv)


if __name__ == "__main__":
    runtests()
