from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from vote.views import VoteMixin

from .models import Comment
from .serializers import CommentSerializer


def comments(request):
    comments = Comment.objects.all()
    return render(request, 'test/comments.html', {'comments': comments})


class CommentViewSet(ModelViewSet, VoteMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
