from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class VoteManger(models.Manager):
    def filter(self, *args, **kwargs):
        if 'content_object' in kwargs:
            content_object = kwargs.pop('content_object')
            content_type = ContentType.objects.get_for_model(content_object)
            kwargs.update({
                'content_type': content_type,
                'object_id': content_object.pk
            })

        return super(VoteManger, self).filter(*args, **kwargs)


class Vote(models.Model):
    user_id = models.BigIntegerField()
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    create_at = models.DateTimeField(auto_now_add=True)

    objects = VoteManger()

    class Meta:
        unique_together = ('user_id', 'content_type', 'object_id')
        index_together = ('content_type', 'object_id')

    @classmethod
    def votes_for(cls, model, instance=None):
        ct = ContentType.objects.get_for_model(model)
        kwargs = {
            "content_type": ct
        }
        if instance is not None:
            kwargs["object_id"] = instance.pk

        return cls.objects.filter(**kwargs)
