from django.db import models, transaction, IntegrityError
from django.db.models.query import QuerySet
from django.db.utils import OperationalError
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from vote.utils import instance_required, add_field_to_objects

UP = 0
DOWN = 1


class VotedQuerySet(QuerySet):

    """
    if call votes.annotate with an `user` argument then add `is_voted` to each
    instance.
    """

    def __init__(self, model=None, query=None, using=None, user_id=None,
                 hints=None):

        self.user_id = user_id
        super(VotedQuerySet, self).__init__(model, query, using, hints)

    def __iter__(self):
        super(VotedQuerySet, self).__iter__()

        if self.user_id is None:
            return iter(self._result_cache)

        objects = self._result_cache
        user_id = self.user_id

        objects = add_field_to_objects(self.model, objects, user_id)

        self._result_cache = objects
        return iter(objects)

    def _clone(self):
        c = super(VotedQuerySet, self)._clone()
        c.user_id = self.user_id
        return c


class _VotableManager(models.Manager):

    def __init__(self, through, model, instance, field_name='votes'):
        self.through = through
        self.model = model
        self.instance = instance
        self.field_name = field_name

    def vote(self, user_id, action):
        try:
            with transaction.atomic():
                self.instance = self.model.objects.select_for_update().get(
                    pk=self.instance.pk)

                content_type = ContentType.objects.get_for_model(self.model)
                try:
                    vote = self.through.objects.get(user_id=user_id,
                                                    content_type=content_type,
                                                    object_id=self.instance.pk)
                    if vote.action == action:
                        return False
                    vote.action = action
                    vote.save()

                    # will delete your up if you vote down some instance that
                    # you have vote up
                    voted_field = self.through.ACTION_FIELD.get(
                        int(not action))
                    setattr(self.instance, voted_field,
                            getattr(self.instance, voted_field) - 1)
                except self.through.DoesNotExist:
                    self.through.objects.create(user_id=user_id,
                                                content_type=content_type,
                                                object_id=self.instance.pk,
                                                action=action)

                statistics_field = self.through.ACTION_FIELD.get(action)
                setattr(self.instance, statistics_field,
                        getattr(self.instance, statistics_field) + 1)

                self.instance.save()

            return True
        except (OperationalError, IntegrityError):
            return False

    @instance_required
    def up(self, user_id):
        return self.vote(user_id, action=UP)

    @instance_required
    def down(self, user_id):
        return self.vote(user_id, action=DOWN)

    @instance_required
    def delete(self, user_id):
        try:
            with transaction.atomic():
                content_type = ContentType.objects.get_for_model(self.instance)

                try:
                    # select_for_update will add a write lock here
                    vote = self.through.objects.select_for_update().get(
                        user_id=user_id,
                        content_type_id=content_type.id,
                        object_id=self.instance.id
                    )
                except self.through.DoesNotExist:
                    return False

                self.instance = self.model.objects.select_for_update().get(
                    pk=self.instance.pk)
                statistics_field = self.through.ACTION_FIELD.get(vote.action)
                setattr(self.instance, statistics_field,
                        getattr(self.instance, statistics_field) - 1)

                self.instance.save()

                vote.delete()

            return True
        except (OperationalError, IntegrityError):
            # concurrent request may decrease num_vote field to negative
            return False

    @instance_required
    def get(self, user_id):
        return self.through.objects.filter(
            user_id=user_id,
            content_object=self.instance,
        ).first()

    @instance_required
    def exists(self, user_id, action=UP):
        return self.through.objects.filter(
            user_id=user_id,
            content_object=self.instance,
            action=action
        ).exists()

    def all(self, user_id, action=UP):
        content_type = ContentType.objects.get_for_model(self.model)

        object_ids = self.through.objects.filter(
            user_id=user_id,
            content_type=content_type,
            action=action).values_list('object_id', flat=True)

        return self.model.objects.filter(pk__in=list(object_ids))

    def count(self, action=UP):
        return self.through.votes_for(self.model,
                                      self.instance, action).count()

    def user_ids(self, action=UP):
        return self.through.votes_for(
            self.model, self.instance, action
        ).order_by('-create_at').values_list('user_id', 'create_at')

    def annotate(self, queryset=None, user_id=None,
                 reverse=True, sort=True):

        if queryset is not None:
            queryset = queryset
        else:
            queryset = self.model.objects.all()

        if sort:
            order = reverse and '-%s' % 'vote_score' or 'vote_score'
            queryset = queryset.order_by(order, '-id')

        return VotedQuerySet(model=queryset.model, query=queryset.query,
                             user_id=user_id)

    def vote_by(self, user_id, queryset=None, ids=None):
        if queryset is None and ids is None:
            raise ValueError("queryset or ids can not be None")

        if ids is not None:
            objects = self.model.objects.filter(id__in=ids)
            objects = sorted(objects, key=lambda x: ids.index(x.id))

            return add_field_to_objects(self.model, objects, user_id)
        else:
            return VotedQuerySet(model=queryset.model, query=queryset.query,
                                 user_id=user_id)


class VotableManager(GenericRelation):

    def __init__(self, through=None, manager=_VotableManager, **kwargs):
        from vote.models import Vote
        self.through = Vote if not through else through
        self.manager = manager
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('Votes'))
        super(VotableManager, self).__init__(self.through, **kwargs)

    def __get__(self, instance, model):
        if instance is not None and instance.pk is None:
            raise ValueError(
                "%s objects need to have a primary key value "
                "before you can access their votes." % model.__name__)

        manager = self.manager(
            through=self.through,
            model=model,
            instance=instance,
            field_name=self.name,
        )

        return manager

    def contribute_to_class(self, cls, name):
        super(VotableManager, self).contribute_to_class(cls, name)
        setattr(cls, name, self)
