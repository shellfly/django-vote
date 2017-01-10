from __future__ import absolute_import

from django import template
from django.contrib.auth.models import AnonymousUser

from vote.models import Vote

register = template.Library()


@register.simple_tag
def vote_exists(model, user=AnonymousUser(), action=Vote.UP):
    if user.is_anonymous():
        return False
    return model.votes.exists(user.pk, action=action)
