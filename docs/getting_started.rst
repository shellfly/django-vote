Getting Started
===============

To get started using ``django-vote`` simply install it with
``pip``::

    $ pip install django-vote


Add ``"vote"`` to your project's ``INSTALLED_APPS`` setting.

 
And then to any model you want vote on do the following::

    from django.db import models

    from vote.models import VoteModel

  
    class Comment(VoteModel,models.Model):
        # ... fields here
    
Run::

    ./manage.py makemigrations
    ./manage.py migrate
