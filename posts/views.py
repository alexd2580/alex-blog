from django.shortcuts import get_object_or_404, render

from .models import Post


def index(request):
    published_posts = Post.objects.filter(draft=False).order_by('-publication_date')[:20]
    return render(request, 'posts/index.html', {'published_posts': published_posts})


def detail(request, post_id):
    post = get_object_or_404(Post.objects.filter(draft=False), pk=post_id)
    return render(request, 'posts/detail.html', {'post': post})
