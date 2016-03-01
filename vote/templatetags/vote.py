from django import template

register = template.Library()

@register.simple_tag
def vote_exists(model, user):
    return model.votes.exists(user)
