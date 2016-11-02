from functools import wraps
from django.contrib.contenttypes.models import ContentType
from vote.models import Vote


def instance_required(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if self.instance is None:
            error = "Can't call %s with a non-instance manager" % func.__name__
            raise TypeError(error)

        return func(self, *args, **kwargs)

    return inner


def add_field_to_objects(model, objects, user_id, field='is_voted'):
    content_type = ContentType.objects.get_for_model(model)
    object_ids = [r.id for r in objects]

    voted_object_ids = Vote.objects.filter(
        user_id=user_id,
        content_type=content_type,
        object_id__in=object_ids
    ).values_list("object_id", flat=True)

    for r in objects:
        setattr(r, field, r.pk in voted_object_ids)

    return objects
