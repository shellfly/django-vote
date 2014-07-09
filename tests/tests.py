from __future__ import absolute_import
from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User

from vote.models import Vote
from vote.compat import atomic
from tests.models import Comment, CustomVoteComment 

class VoteTest(TestCase):
    through = Vote
    model = Comment 
    field_name = 'votes'

    def setUp(self):
        self.user1 = User.objects.create_user("test1", "test1@test.com", '111111')
        self.user2 = User.objects.create_user("test2", "test2@test.com", '111111')
        self.user3 = User.objects.create_user("test3", "test3@test.com", '111111')

    def tearDown(self):
        self.model.objects.all().delete()
        self.through.objects.all().delete()
        User.objects.all().delete()
        
    def call_api(self, api_name, model=None, *args, **kwargs):
        model = model or self.model
        votes = getattr(model, self.field_name)
        api = getattr(votes, api_name)
        return api(*args, **kwargs)

    def test_vote_up(self):
        comment = self.model.objects.create(user=self.user1, content="I'm a comment")
        # comment.votes.up(self.user2)
        self.call_api('up', comment, self.user2)
        try:
            with atomic():
                #comment.votes.up(self.user2)
                self.call_api('up', comment, self.user2)
            # should not access here 
            self.assertTrue(0)
        except IntegrityError:
            pass
            
        self.assertEqual(self.call_api('count', comment), 1)

    def test_vote_down(self):
        comment = self.model.objects.create(user=self.user1, content="I'm a comment")
        # no votes yet, no exception raised
        self.assertEqual(self.call_api('count'), 0)
        self.call_api('down', comment, self.user2)
                
        self.call_api('up', comment, self.user2)
        self.assertEqual(self.call_api('count', comment), 1)
        self.call_api('down', comment, self.user2)
        self.assertEqual(self.call_api('count', comment), 0)

    def test_vote_exists(self):
        comment = self.model.objects.create(user=self.user1, content="I'm a comment")
        self.assertFalse(self.call_api('exists', comment, self.user2))
        self.call_api('up', comment, self.user2)
        self.assertTrue(self.call_api('exists', comment, self.user2))
        
    def test_vote_count(self):
        comment1 = self.model.objects.create(user=self.user1, content="I'm a comment")
        comment2 = self.model.objects.create(user=self.user1, content="I'm a comment too")
        self.call_api('up', comment1, self.user2)
        self.call_api('up', comment2, self.user2)
        self.assertEqual(self.call_api('count', comment1), 1)
        self.assertEqual(self.call_api('count', comment2), 1)
        self.assertEqual(self.call_api('count'), 2)

    def test_vote_annotate(self):
        comments = [
            self.model(user=self.user1, content="I'm a comment, sequence %s" % i) for i in range(10)
            ]
        self.model.objects.bulk_create(comments)
        comments = list(self.model.objects.all())
        
        comment1 = comments[0]
        self.call_api('up', comment1, self.user2)

        comment2 = comments[1]
        self.call_api('up', comment2, self.user2)
        self.call_api('up', comment2, self.user3)

        # queryset=None, user=None
        # comments = self.model.votes.annotate()
        comments = self.call_api('annotate')

        self.assertEqual(comments[0].pk, comment2.pk)
        self.assertEqual(comments[1].pk, comment1.pk)
        
        # comments = list(self.model.votes.annotate(reverse=False))
        comments = list(self.call_api('annotate', reverse=False))
        self.assertEqual(comments[-1].pk, comment2.pk)
        self.assertEqual(comments[-2].pk, comment1.pk)
        
        for comment in comments:
            self.assertTrue(hasattr(comment, 'num_votes'))

        # call annotate with queryset and user
        comments = self.model.objects.filter(user=self.user1)
        # comments = self.model.votes.annotate(comments, user=self.user2)
        comments = self.call_api('annotate', queryset=comments, user=self.user2)
        self.assertEqual(comments[0].pk, comment2.pk)
        self.assertEqual(comments[1].pk, comment1.pk)
        for comment in comments:
            self.assertTrue(hasattr(comment, 'num_votes'))
            self.assertTrue(hasattr(comment, 'is_voted'))
            if comment.pk in (comment1.pk, comment2.pk):
                self.assertTrue(comment.is_voted)
            else:
                self.assertFalse(comment.is_voted)

class CustomVoteTest(VoteTest):
    through = Vote
    model = CustomVoteComment
    field_name = 'custom_votes'
