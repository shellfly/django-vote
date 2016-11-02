from django.db import models
from vote.managers import VotableManager


# Create your models here.
class Comment(models.Model):
    user_id = models.BigIntegerField()
    content = models.TextField()
    num_vote = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    votes = VotableManager()


class CustomVoteComment(models.Model):
    user_id = models.BigIntegerField()
    content = models.TextField()
    num_vote = models.PositiveIntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    custom_votes = VotableManager(extra_field='num_vote')
