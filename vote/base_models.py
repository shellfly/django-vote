from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

UP = 0
DOWN = 1


class VoteManager(models.Manager):

    def filter(self, *args, **kwargs):
        if 'content_object' in kwargs:
            content_object = kwargs.pop('content_object')
            content_type = ContentType.objects.get_for_model(content_object)
            kwargs.update({
                'content_type': content_type,
                'object_id': content_object.pk
            })

        return super(VoteManager, self).filter(*args, **kwargs)


class AbstractVote(models.Model):
    ACTION_FIELD = {
        UP: 'num_vote_up',
        DOWN: 'num_vote_down'
    }

    user_id = models.BigIntegerField()
    content_type = models.ForeignKey(
        ContentType,
        related_name='+',
        on_delete=models.CASCADE
    )
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()
    action = models.PositiveSmallIntegerField(default=UP)
    create_at = models.DateTimeField(auto_now_add=True)

    objects = VoteManager()

    class Meta:
        abstract = True
        index_together = ('content_type', 'object_id')

    @classmethod
    def votes_for(cls, model, instance=None, action=UP):
        ct = ContentType.objects.get_for_model(model)
        kwargs = {
            "content_type": ct,
            "action": action
        }
        if instance is not None:
            kwargs["object_id"] = instance.pk

        return cls.objects.filter(**kwargs)
