from rest_framework.decorators import action
from rest_framework.views import Response

from vote.signals import post_voted


class VoteMixin:
    def get_instance(self, pk):
        return self.queryset.get(pk=pk)

    @action(detail=True, methods=('post', 'delete'))
    def vote(self, request, pk):
        obj = self.get_instance(pk)
        user_id = request.user.pk
        if request.method.lower() == 'post':
            action = request.data.get('action', 'up')
            voted = getattr(obj.votes, action)(user_id)
            if voted:
                post_voted.send(sender=self.queryset.model,
                                obj=obj,
                                user_id=user_id,
                                action=action)
            else:
                return Response(data={}, status=409)
        else:
            deleted = obj.votes.delete(user_id)
            if deleted:
                post_voted.send(sender=self.queryset.model,
                                obj=obj,
                                user_id=user_id,
                                action='delete')
        return Response({})
