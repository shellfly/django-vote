from __future__ import absolute_import
from django.test import TestCase
from django.db import IntegrityError
from django.contrib.auth.models import User

from vote.models import Vote
from tests.models import Comment

class VoteTest(TestCase):
    through = Vote
    
    def setUp(self):
        self.user1 = User.objects.create_user("test1", "test1@test.com", '111111')
        self.user2 = User.objects.create_user("test2", "test2@test.com", '111111')
        self.user3 = User.objects.create_user("test3", "test3@test.com", '111111')

    def tearDown(self):
        Comment.objects.all().delete()
        self.through.objects.all().delete()
        User.objects.all().delete()
        
    def test_vote_up(self):
        comment = Comment.objects.create(user=self.user1, content="I'm a comment")
        comment.votes.up(self.user2)
        try:
            comment.votes.up(self.user2)
            # should not access here 
            self.assertTrue(0)
        except IntegrityError:
            pass
            
        self.assertEqual(comment.votes.count(), 1)

    def test_vote_down(self):
        comment = Comment.objects.create(user=self.user1, content="I'm a comment")
        # no votes yet, no exception raised
        self.assertEqual(comment.votes.count(), 0)
        comment.votes.down(self.user2)
                
        comment.votes.up(self.user2)
        self.assertEqual(comment.votes.count(), 1)
        comment.votes.down(self.user2)
        self.assertEqual(comment.votes.count(), 0)

    def test_vote_exists(self):
        comment = Comment.objects.create(user=self.user1, content="I'm a comment")
        self.assertFalse(comment.votes.exists(self.user2))
        comment.votes.up(self.user2)
        self.assertTrue(comment.votes.exists(self.user2))
        
    def test_vote_count(self):
        comment1 = Comment.objects.create(user=self.user1, content="I'm a comment")
        comment2 = Comment.objects.create(user=self.user1, content="I'm a comment too")
        comment1.votes.up(self.user2)
        comment2.votes.up(self.user2)
        self.assertEqual(comment1.votes.count(), 1)
        self.assertEqual(comment2.votes.count(), 1)
        self.assertEqual(Comment.votes.count(), 2)

    def test_vote_annotate(self):
        comments = [
            Comment(user=self.user1, content="I'm a comment, sequence %s" % i) for i in range(10)
            ]
        Comment.objects.bulk_create(comments)
        comments = list(Comment.objects.all())
        
        comment1 = comments[0]
        comment1.votes.up(self.user2)

        comment2 = comments[1]
        comment2.votes.up(self.user2)
        comment2.votes.up(self.user3)

        # queryset=None, user=None
        comments = Comment.votes.annotate()
        self.assertEqual(comments[0].pk, comment2.pk)
        self.assertEqual(comments[1].pk, comment1.pk)
        
        comments = list(Comment.votes.annotate(reverse=False))
        self.assertEqual(comments[-1].pk, comment2.pk)
        self.assertEqual(comments[-2].pk, comment1.pk)
        
        for comment in comments:
            self.assertTrue(hasattr(comment, 'num_votes'))

        # call annorate with queryset and user
        comments = Comment.objects.filter(user=self.user1)
        comments = Comment.votes.annotate(comments, user=self.user2)
        self.assertEqual(comments[0].pk, comment2.pk)
        self.assertEqual(comments[1].pk, comment1.pk)
        for comment in comments:
            self.assertTrue(hasattr(comment, 'num_votes'))
            self.assertTrue(hasattr(comment, 'is_voted'))
            if comment.pk in (comment1.pk, comment2.pk):
                self.assertTrue(comment.is_voted)
            else:
                self.assertFalse(comment.is_voted)
        
        
