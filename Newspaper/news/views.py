from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from .models import Author, Post, Category, Comment


def index(request):
    return render(request, 'news/index.html')


def news_list(request):
    news = Post.objects.filter(type='NW').order_by('-timestamp')[:10]
    out = ', '.join([n.title for n in news])
    return HttpResponse(out)


def news_details(request, news_id):
    return HttpResponse(f'Here be news details for {news_id}')

