from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Author, Post, Category, Comment


def news_index(request):
    posts_list = get_list_or_404(Post.objects.order_by('timestamp'))
    context = {'posts_list': posts_list}
    return render(request, 'news/index.html', context)


def news_detail(request, news_id):
    post = get_object_or_404(Post, pk=news_id)
    return render(request, 'news/detail.html', {'post': post})

