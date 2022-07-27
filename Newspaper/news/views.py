from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import generic
from .models import Author, Post, Category, Comment


class IndexView(generic.ListView):
    model = Post
    ordering = 'timestamp'
    paginate_by = 2
    template_name = 'news/index.html'
    context_object_name = 'posts_list'


class DetailView(generic.DetailView):
    model = Post
    template_name = 'news/detail.html'

