Getting Started
===============

To get started using ``django-vote`` simply install it with
``pip``::

    $ pip install django-vote


Add ``"vote"`` to your project's ``INSTALLED_APPS`` setting.

Run::
    
    ./manage.py syncdb
 
And then to any model you want vote on do the following::

    from django.db import models

    from vote.managers import VotableManager

    class Comment(models.Model):
        # ... fields here

        votes = VotableManager()

