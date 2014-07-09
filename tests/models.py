from django.db import models

from vote.compat import AUTH_USER_MODEL
from vote.managers import VotableManager

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    votes = VotableManager()

class CustomVoteComment(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL)
    content = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    custom_votes = VotableManager()

