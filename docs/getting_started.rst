Getting Started
===============

To get started using ``django-vote`` simply install it with
``pip``::

    $ pip install django-vote


Add ``"vote"`` to your project's ``INSTALLED_APPS`` setting.

Run::
    
    ./manage.py migrate
 
And then to any model you want vote on do the following::

    from django.db import models

    from vote.managers import VotableManager

  
    class Comment(models.Model):
        # ... fields here

        votes = VotableManager()



If you want to save number of votes directly on original model::

    from django.db import models

    from vote.managers import VotableManager

  
    class Comment(models.Model):
        # ... fields here
        num_votes = models.PositiveIntegerField(default=0)
        votes = VotableManager(extra_field='num_votes')
