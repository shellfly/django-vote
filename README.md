## Django Vote

``django-vote`` is a simple Django app to conduct vote for django model.

This project is inspired by [django-taggit](https://github.com/alex/django-taggit)

[![Build Status](https://travis-ci.org/shanbay/django-vote.svg?branch=develop)](https://travis-ci.org/shanbay/django-vote)
[![Codecov](https://codecov.io/gh/shanbay/django-vote/coverage.svg?branch=master)](https://codecov.io/gh/shanbay/django-vote?branch=master)

### Quick start

#### Install `django-vote` by pip

```shell
pip install django-vote
```

#### Add `'vote'` to your `INSTALLED_APPS` setting like this

```python
INSTALLED_APPS = (
  ...
  'vote',
)
```

#### Run migrate 

```shell
manage.py migrate
```

#### Declare vote field to the model you want to vote

```python
from vote.managers import VotableManager

class ArticleReview(models.Model):
    ...
    votes = VotableManager()
```

#### Use vote API

```python
review = ArticleReview.objects.get(pk=1)

# Adds a new vote to the object
review.votes.up(user_id)

# Removes vote to the object
review.votes.down(user_id)

# Check if the user already voted the object
review.votes.exists(user_id)

# Returns all instances voted by user
Review.votes.all(user_id)

# Returns the number of votes for the object
review.votes.count()

# Returns a list of users who voted and their voting date
review.votes.users()
```

``django-vote`` now requires Django 1.7 or greater. (for Django < 1.7, please install previous release `django-vote==1.1.3`)
