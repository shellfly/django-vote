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
To add ``num_vote`` and ``is_voted`` to all instance in a queryset, you can call the ``annotate`` API like so::

    >>> comments = Comment.objects.filter(article__id=article_id)
    >>> Comment.votes.annotate(comments, user=user)



