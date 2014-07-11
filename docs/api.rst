The API
=======

After you've got your ``VotableManager`` added to your model you can start
playing around with the API.

.. class:: VotableManager([through=None, verbose_name="Votes"])

    :param verbose_name: The verbose_name for this field.
    :param through: The through model

    .. method:: up(user)

        This adds a vote to an object by the ``user``. ``IntegrityError`` will be raised if the user has voted before::

            >>> comments.votes.up(user)

    .. method:: down(user)

        Removes the vote from an object. No exception is raised if the user 
        doesn't have voted the object.

    .. method:: count()

        The count of  all votes for an object.

    .. method:: annotate(queryset=None, user=None)

        Add annotation data to the ``queyset``

Aggregation
~~~~~~~~~~~
Django does not support aggregation with GenericRelation `currently <https://docs.djangoproject.com/en/1.6/ref/contrib/contenttypes/#generic-relations-and-aggregation>`_
but you still can use `annotate`::

    >>> Comment.objects.filter(article__id=article_id).annotate(num_votes=Count('votes__user'))


Or you can call the ``annotate`` API like so, this will add `num_votes` and `is_voted` to each instance::

    >>> comments = Comment.objects.filter(article__id=article_id)
    >>> Comment.votes.annotate(comments, user=user)



