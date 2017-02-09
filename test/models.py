from django.db import models
from vote.models import VoteModel


# Create your models here.
class Comment(VoteModel):
    user_id = models.BigIntegerField()
    content = models.TextField()
    num_vote = models.IntegerField(default=0)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
