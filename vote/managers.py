from django.db import models, transaction, IntegrityError
from django.db.models import Count, F
from django.db.models.query import QuerySet
from django.db.utils import OperationalError
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from vote.models import Vote
from vote.utils import instance_required, add_field_to_objects


class VotedQuerySet(QuerySet):
    """
    if call votes.annotate with an `user` argument then add `is_voted` to each
    instance.
    """

    def __init__(self, model=None, query=None, using=None, user_id=None,
                 hints=None, field='is_voted'):

        self.user_id = user_id
        self.vote_field = field
        super(VotedQuerySet, self).__init__(model, query, using, hints)

    def __iter__(self):
        super(VotedQuerySet, self).__iter__()

        if self.user_id is None:
            return iter(self._result_cache)

        objects = self._result_cache
        user_id = self.user_id

        objects = add_field_to_objects(self.model, objects, user_id,
                                       field=self.vote_field)

        self._result_cache = objects
        return iter(objects)

    def _clone(self):
        c = super(VotedQuerySet, self)._clone()
        c.user_id = self.user_id
        return c


class _VotableManager(models.Manager):
    def __init__(self, through, model, instance, field_name='votes',
                 extra_field=None):
        self.through = through
        self.model = model
        self.instance = instance
        self.field_name = field_name
        self.extra_field = extra_field

    @instance_required
    def up(self, user_id):
        try:
            with transaction.atomic():
                self.through(user_id=user_id,
                             content_object=self.instance).save()

                if self.extra_field:
                    setattr(self.instance, self.extra_field,
                            F(self.extra_field)+1)

                    self.instance.save()

            return True
        except (OperationalError, IntegrityError):
            return False

    @instance_required
    def down(self, user_id):
        try:
            with transaction.atomic():
                content_type = ContentType.objects.get_for_model(self.instance)

                try:
                    vote = self.through.objects.select_for_update().get(
                        user_id=user_id,
                        content_type_id=content_type.id,
                        object_id=self.instance.id
                    )
                except self.through.DoesNotExist:
                    return False

                if self.extra_field:
                    setattr(self.instance, self.extra_field,
                            F(self.extra_field)-1)

                    self.instance.save()

                vote.delete()

            return True
        except (OperationalError, IntegrityError):
            # concurrent request may decrease num_vote field to negative
            return False

    @instance_required
    def exists(self, user_id):
        return self.through.objects.filter(
            user_id=user_id,
            content_object=self.instance
        ).exists()

    def all(self, user_id):
        content_type = ContentType.objects.get_for_model(self.model)

        object_ids = self.through.objects.filter(
            user_id=user_id,
            content_type=content_type).values_list('object_id', flat=True)

        return self.model.objects.filter(pk__in=list(object_ids))

    def count(self):
        return self.through.votes_for(self.model, self.instance).count()

    def user_ids(self):
        return self.through.votes_for(
            self.model, self.instance
        ).order_by('-create_at').values_list('user_id', 'create_at')

    def annotate(self, queryset=None, user_id=None, annotation='num_votes',
                 reverse=True, sort=True):

        kwargs = {annotation: Count('%s__user_id' % self.field_name)}

        if queryset is not None:
            queryset = queryset
        else:
            queryset = self.model.objects.all()

        queryset = queryset.annotate(**kwargs)

        if sort:
            order = reverse and '-%s' % annotation or annotation
            queryset = queryset.order_by(order, '-id')

        return VotedQuerySet(model=queryset.model, query=queryset.query,
                             user_id=user_id)

    def vote_by(self, user_id, queryset=None, ids=None, field='is_voted'):
        if queryset is None and ids is None:
            raise ValueError("queryset or ids can not be None")

        if ids is not None:
            objects = self.model.objects.filter(id__in=ids)
            objects = sorted(objects, key=lambda x: ids.index(x.id))

            return add_field_to_objects(self.model, objects, user_id,
                                        field=field)
        else:
            return VotedQuerySet(model=queryset.model, query=queryset.query,
                                 user_id=user_id, field=field)


class VotableManager(GenericRelation):
    def __init__(self, through=Vote, manager=_VotableManager, **kwargs):
        self.through = through
        self.manager = manager
        kwargs['verbose_name'] = kwargs.get('verbose_name', _('Votes'))
        self.extra_field = kwargs.pop('extra_field', None)
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
            extra_field=self.extra_field,
        )

        return manager

    def contribute_to_class(self, cls, name):
        super(VotableManager, self).contribute_to_class(cls, name)
        setattr(cls, name, self)
