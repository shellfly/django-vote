=====
Vote
=====

Vote is a simple Django app to conduct vote for each model


Quick start
-----------

1. Install ``django-vote`` by pip::
    
    pip install django-vote 

2. Add ``'vote'`` to your ``INSTALLED_APPS`` setting like this::

    INSTALLED_APPS = (
    ...
    'vote',
    )

3. Run ``python manage.py syncdb`` to create the vote models.


4. Declare vote field to the model you want to vote::

    from vote.manager import VotableManager

    class ArticleReview(models.Model):
        ...
        votes = VotableManager()

5. Use vote API::

    >>> review = ArticleReview.objects.get(pk=1)
    >>> review.votes.up(user)
    >>> review.votes.down(user)
