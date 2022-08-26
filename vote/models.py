from django.db import models
from vote.base_models import AbstractVote
from vote.managers import VotableManager
try:
    from swapper import swappable_setting
except ImportError:
    swappable_setting = None


class Vote(AbstractVote):

    class Meta:
        abstract = False
        unique_together = ('user_id', 'content_type', 'object_id', 'action')
        index_together = ('content_type', 'object_id')
        swappable = None
        if swappable_setting:
            swappable = swappable_setting('vote', 'Vote')


class VoteModel(models.Model):
    vote_score = models.IntegerField(default=0, db_index=True)
    num_vote_up = models.PositiveIntegerField(default=0, db_index=True)
    num_vote_down = models.PositiveIntegerField(default=0, db_index=True)
    votes = VotableManager()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.vote_score = self.calculate_vote_score
        super(VoteModel, self).save(*args, **kwargs)

    @property
    def calculate_vote_score(self):
        return self.num_vote_up - self.num_vote_down

    @property
    def is_voted_up(self):
        try:
            return self._is_voted_up
        except AttributeError:
            return False

    @is_voted_up.setter
    def is_voted_up(self, value):
        self._is_voted_up = value

    @property
    def is_voted_down(self):
        try:
            return self._is_voted_down
        except AttributeError:
            return False

    @is_voted_down.setter
    def is_voted_down(self, value):
        self._is_voted_down = value
