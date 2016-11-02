from django.shortcuts import render

from test.models import Comment


def comments(request):
    comments = Comment.objects.all()
    return render(request, 'test/comments.html', {'comments': comments})
