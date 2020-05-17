REST API
========

There is a `VoteMixin` for you to easily add rest api to conduct vote::

    from vote.views import VoteMixin

    class CommentViewSet(VoteMixin,ModelViewSet):
        # ... fields here
