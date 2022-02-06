## Django Vote

``django-vote`` is a simple Django app to conduct vote for django model.

This project is inspired by [django-taggit](https://github.com/alex/django-taggit)

![Ci](https://github.com/shellfly/django-vote/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/gh/shellfly/django-vote/branch/master/graph/badge.svg)](https://codecov.io/gh/shellfly/django-vote)
[![PyPI version](https://badge.fury.io/py/django-vote.svg)](https://badge.fury.io/py/django-vote)

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

#### Add `VoteModel` to the model you want to vote

```python
from vote.models import VoteModel

class ArticleReview(VoteModel, models.Model):
    ...
```

#### Run migrate

```shell
manage.py makemigrations
manage.py migrate
```

#### Use vote API

```python
review = ArticleReview.objects.get(pk=1)

# Up vote to the object
review.votes.up(user_id)

# Down vote to the object
review.votes.down(user_id)

# Removes a vote from the object
review.votes.delete(user_id)

# Check if the user already voted (up) the object
review.votes.exists(user_id)

# Check if the user already voted (down) the object
# import UP, DOWN from vote.models
review.votes.exists(user_id, action=DOWN)

# Returns the number of votes for the object
review.votes.count()

# Returns a list of users who voted and their voting date
review.votes.user_ids()


# Returns all instances voted by user
Review.votes.all(user_id)

```

#### Use `VoteMixin` for REST API

``` python
class CommentViewSet(ModelViewSet, VoteMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
```

```sh
POST /api/comments/{id}/vote/
POST /api/comments/{id}/vote/ {"action":"down"}
DELETE /api/comments/{id}/vote/
```
