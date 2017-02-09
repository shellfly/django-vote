from __future__ import absolute_import
from django.test import TestCase
from django.contrib.auth.models import User
from vote.models import Vote, UP, DOWN
from test.models import Comment


class VoteTest(TestCase):
    through = Vote
    model = Comment
    field_name = 'votes'

    def setUp(self):
        self.user1 = User.objects.create_user("test1", "test1@test.com",
                                              '111111')
        self.user2 = User.objects.create_user("test2", "test2@test.com",
                                              '111111')
        self.user3 = User.objects.create_user("test3", "test3@test.com",
                                              '111111')

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
        comment = self.model.objects.create(user_id=self.user1.pk,
                                            content="I'm a comment")

        self.call_api('up', comment, self.user2.pk)
        self.assertEqual(self.call_api('count', comment, UP), 1)

        # call up again, will not increase count
        res = self.call_api('up', comment, self.user2.pk)
        self.assertEqual(res, False)
        self.assertEqual(self.call_api('count', comment, UP), 1)

    def test_vote_down(self):
        comment = self.model.objects.create(user_id=self.user1.pk,
                                            content="I'm a comment")

        # no votes yet, no exception raised
        self.assertEqual(self.call_api('count', comment, DOWN), 0)
        self.call_api('down', comment, self.user2.pk)
        self.assertEqual(self.call_api('count', comment, DOWN), 1)

        self.call_api('up', comment, self.user2.pk)
        self.assertEqual(self.call_api('count', comment, UP), 1)
        self.call_api('down', comment, self.user2.pk)
        self.assertEqual(self.call_api('count', comment, DOWN), 1)

    def test_vote_delete(self):
        comment = self.model.objects.create(user_id=self.user1.pk,
                                            content="I'm a comment")

        self.call_api('up', comment, self.user2.pk)
        self.assertEqual(self.call_api('count', comment, UP), 1)
        self.call_api('delete', comment, self.user2.pk)
        self.assertEqual(self.call_api('count', comment, UP), 0)

    def test_vote_exists(self):
        comment = self.model.objects.create(user_id=self.user1.pk,
                                            content="I'm a comment")
        self.assertFalse(self.call_api('exists', comment, self.user2.pk,
                                       UP))
        self.call_api('up', comment, self.user2.pk)
        self.assertTrue(self.call_api('exists', comment,
                                      self.user2.pk, UP))

    def test_vote_all(self):
        comment = self.model.objects.create(user_id=self.user1.pk,
                                            content="I'm a comment")
        self.assertFalse(self.call_api('exists', comment, self.user2.pk))
        self.call_api('up', comment, self.user2.pk)
        self.assertEqual(len(self.call_api('all', comment, self.user2.pk)), 1)

    def test_vote_count(self):
        comment1 = self.model.objects.create(user_id=self.user1.pk,
                                             content="I'm a comment")
        comment2 = self.model.objects.create(user_id=self.user1.pk,
                                             content="I'm a comment too")
        self.call_api('up', comment1, self.user2.pk)
        self.call_api('up', comment2, self.user2.pk)
        self.assertEqual(self.call_api('count', comment1), 1)
        self.assertEqual(self.call_api('count', comment2), 1)
        self.assertEqual(self.call_api('count'), 2)

    def test_user_ids(self):
        comment = self.model.objects.create(user_id=self.user1.pk,
                                            content="I'm a comment")
        self.call_api('up', comment, self.user1.pk)
        self.assertEqual(len(list(self.call_api('user_ids', comment))), 1)
        
        self.call_api('up', comment, self.user2.pk)
        self.assertEqual(len(list(self.call_api('user_ids', comment))), 2)
        
    def test_vote_annotate(self):
        comments = [
            self.model(
                user_id=self.user1.pk,
                content="I'm a comment, sequence %s" % i) for i in range(10)
            ]

        self.model.objects.bulk_create(comments)
        comments = list(self.model.objects.all())

        comment1 = comments[0]
        self.call_api('up', comment1, self.user2.pk)

        comment2 = comments[1]
        self.call_api('up', comment2, self.user2.pk)
        self.call_api('up', comment2, self.user3.pk)

        # queryset=None, user_id=None
        comments = self.call_api('annotate')

        self.assertEqual(comments[0].pk, comment2.pk)
        self.assertEqual(comments[1].pk, comment1.pk)

        comments = list(self.call_api('annotate', reverse=False))
        self.assertEqual(comments[-1].pk, comment2.pk)
        self.assertEqual(comments[-2].pk, comment1.pk)

        for comment in comments:
            self.assertTrue(hasattr(comment, 'vote_score'))

        # call annotate with queryset and user_id
        comments = self.model.objects.filter(user_id=self.user1.pk)
        comments = self.call_api('annotate', queryset=comments,
                                 user_id=self.user2.pk)
        self.assertEqual(comments[0].pk, comment2.pk)
        self.assertEqual(comments[1].pk, comment1.pk)

        for comment in comments:
            self.assertTrue(hasattr(comment, 'vote_score'))
            self.assertTrue(hasattr(comment, 'is_voted_up'))
            self.assertTrue(hasattr(comment, 'is_voted_down'))
            if comment.pk in (comment1.pk, comment2.pk):
                self.assertTrue(comment.is_voted_up)
            else:
                self.assertFalse(comment.is_voted_up)

    def test_objects_with_status(self):
        comments = [
            self.model(
                user_id=self.user1.pk,
                content="I'm a comment, sequence %s" % i) for i in range(10)
            ]

        self.model.objects.bulk_create(comments)
        comments = list(self.model.objects.all())

        comment1 = comments[0]
        self.call_api('up', comment1, self.user2.pk)

        comment2 = comments[1]
        self.call_api('up', comment2, self.user2.pk)
        self.call_api('up', comment2, self.user3.pk)

        comment_ids = [comment2.id, comment1.id]

        votes = getattr(self.model, self.field_name)
        comments = votes.vote_by(self.user2.pk, ids=comment_ids)

        self.assertEqual(comments[0].id, comment2.id)
        for comment in comments:
            self.assertTrue(hasattr(comment, 'is_voted_up'))
            self.assertTrue(hasattr(comment, 'is_voted_down'))

        comment_ids = [comment1.id, comment2.id]

        votes = getattr(self.model, self.field_name)
        comments = votes.vote_by(self.user2.pk, ids=comment_ids)

        self.assertEqual(comments[0].id, comment1.id)
        for comment in comments:
            self.assertTrue(hasattr(comment, 'is_voted_up'))
            self.assertTrue(hasattr(comment, 'is_voted_down'))


        comments = votes.vote_by(self.user2.pk, queryset=Comment.objects.all())
        for comment in comments:
            self.assertTrue(hasattr(comment, 'is_voted_up'))
            self.assertTrue(hasattr(comment, 'is_voted_down'))

        self.assertRaises(ValueError, lambda: votes.vote_by(self.user2.pk))

    def test_vote_templatetag(self):
        comments = [
            self.model(
                user_id=self.user1.pk,
                content="I'm a comment, sequence %s" % i) for i in range(5)
            ]

        self.model.objects.bulk_create(comments)
        comments = list(self.model.objects.all())

        comment1 = comments[0]
        self.call_api('up', comment1, self.user1.pk)
        res = self.client.get('/comments/')
        self.client.login(username=self.user1.username, password='111111')
        self.client.get('/comments/')
