from django.db import models
from vote.base_models import AbstractVote
from vote.models import VoteModel


# Create your models here.
class MyVote(AbstractVote):
    '''To test model swapping'''
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = False
        unique_together = ('user_id', 'content_type', 'object_id', 'action')
        index_together = ('content_type', 'object_id')


class Comment(VoteModel):
    user_id = models.BigIntegerField()
    content = models.TextField()
    num_vote = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
