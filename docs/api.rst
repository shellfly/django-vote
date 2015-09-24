The API
=======

After you've got your ``VotableManager`` added to your model you can start
playing around with the API.

.. class:: VotableManager([through=None, verbose_name="Votes", field_name='votes', extra_field=None])

    :param verbose_name: The verbose_name for this field.
    :param through: The through model
    :param field_name: The field name added to the query
    :param extra_field: The field on your model. It will be updated when up or down

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

    .. method:: filter(query, current_user=None, annotation='num_votes', reverse=True)
        
        filter original model, add `num_votes` to the queryset

        if `current_user` is provided, then add `is_voted` to the queryset

Aggregation
~~~~~~~~~~~
Django does not support aggregation with GenericRelation `currently <https://docs.djangoproject.com/en/1.6/ref/contrib/contenttypes/#generic-relations-and-aggregation>`_
but you still can use ``annotate``::

    >>> Comment.objects.filter(article__id=article_id).annotate(num_votes=Count('votes__user'))


Or you can call the ``filter`` API like so, this will add ``num_votes`` and ``is_voted`` to each instance::

    >>> Comment.votes.filter(query={'article__id': article_id}, current_user=user)



