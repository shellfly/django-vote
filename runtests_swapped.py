#!/usr/bin/env python
import sys

from django.conf import settings
from django.core.management import execute_from_command_line
from runtests import configure

if not settings.configured:
    configure()


def runtests_swapped():
    argv = sys.argv[:1] + ["test", "test.tests.VoteTest.test_vote_up"] + sys.argv[1:]
    execute_from_command_line(argv)
    configure(VOTE_VOTE_MODEL='test.MyVote')
    from test.models import Comment, MyVote
    from vote.models import VotableManager
    from vote.utils import _reset_vote_model
    _reset_vote_model()
    # The VoteModel's votes manager has to be updated for the new Vote model
    Comment.votes = VotableManager(MyVote)
    argv = sys.argv[:1] + ["test"] + sys.argv[1:]
    execute_from_command_line(argv)


if __name__ == "__main__":
    runtests_swapped()
