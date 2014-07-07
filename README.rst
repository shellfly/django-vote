=====
Vote
=====

Vote is a simple Django app to conduct vote for each model


Quick start
-----------

1. Add ``"vote"`` to your ``INSTALLED_APPS`` setting like this::

    INSTALLED_APPS = (
    ...
    'polls',
    )

2. Include the polls URLconf in your project urls.py like this::

    2. Run `python manage.py syncdb` to create the vote models.


3. Declare vote filed to the model you want to vote::

    from vote.manager import VotableManager

    class ArticleReview(models.Model):
        ...
        votes = VotableManger()

4. Use vote API::

    >>> review = ArticleReview.get(pk=1)
    >>> review.up(user)
    >>> review.down(user)
