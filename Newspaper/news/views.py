from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.views import generic
from .models import Author, Post, Category, Comment


class IndexView(generic.ListView):
    template_name = 'news/index.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        return Post.objects.order_by('timestamp')

class DetailView(generic.DetailView):
    model = Post
    template_name = 'news/detail.html'

# def news_index(request):
#     posts_list = get_list_or_404(Post.objects.order_by('timestamp'))
#     context = {'posts_list': posts_list}
#     return render(request, 'news/index.html', context)
#
#
# def news_detail(request, news_id):
#     post = get_object_or_404(Post, pk=news_id)
#     return render(request, 'news/detail.html', {'post': post})

