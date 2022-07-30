from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from .models import Author, Post, Category, Comment
from .filters import PostFilter
from .forms import PostForm


class IndexView(generic.ListView):
    # model = Post
    ordering = 'timestamp'
    paginate_by = 10
    template_name = 'news/index.html'
    context_object_name = 'posts_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_post_type'] = self.kwargs['post_type']
        return context

    def get_queryset(self):
        return get_list_or_404(Post.objects.filter(type=self.kwargs['post_type']))


class SearchView(generic.ListView):
    model = Post
    ordering = 'timestamp'
    paginate_by = 10
    template_name = 'news/search.html'
    context_object_name = 'posts_list'

    def get_queryset(self):
        qs = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, qs)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class DetailView(generic.DetailView):
    model = Post
    template_name = 'news/detail.html'


class PostCreate(generic.CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_post_type'] = self.kwargs['post_type']
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = self.kwargs['post_type']
        return super().form_valid(form)


class PostEdit(LoginRequiredMixin, generic.UpdateView):
    # no DRY WTF
    form_class = PostForm
    model = Post
    template_name = 'news/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_post_type'] = self.kwargs['post_type']
        return context


class PostDelete(generic.DeleteView):
    model = Post
    template_name = 'news/delete.html'
    success_url = reverse_lazy('news:news_index')

    def form_valid(self, form):
        if self.kwargs['post_type'] == 'AR':
            self.success_url = reverse_lazy('news:articles_index')
        return super().form_valid(form)
