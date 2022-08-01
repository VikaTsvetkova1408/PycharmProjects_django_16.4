from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views import generic, View
from .models import Author, Post, Category, Comment
from .filters import PostFilter, PostCategoryFilter
from .forms import PostForm


class IndexView(generic.ListView):
    model = Post
    ordering = 'timestamp'
    paginate_by = 10
    template_name = 'news/index.html'
    context_object_name = 'posts_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_post_type'] = self.kwargs['post_type']
        categoies = Category.objects.all()
        context['categories'] = categoies
        current_category_id = self.request.GET.get('category', None)
        if current_category_id:
            context['current_category'] = categoies.filter(pk=current_category_id).first()
        if not isinstance(self.request.user, AnonymousUser):
            context['author'] = Author.objects.filter(user=self.request.user).first()
        return context

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(type=self.kwargs['post_type'])
        self.filterset = PostCategoryFilter(self.request.GET, qs)
        # return get_list_or_404(self.filterset.qs)
        return self.filterset.qs


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not isinstance(self.request.user, AnonymousUser):
            context['author'] = Author.objects.filter(user=self.request.user).first()
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/create.html'
    permission_required = ('news.add_post',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_post_type'] = self.kwargs['post_type']
        return context

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = Author.objects.filter(user=self.request.user).first()
        post.type = self.kwargs['post_type']
        return super().form_valid(form)


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, generic.UpdateView):
    # no DRY WTF
    form_class = PostForm
    model = Post
    template_name = 'news/create.html'
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        obj = super().get_object(**kwargs)
        author = Author.objects.filter(user=self.request.user).first()
        if author != obj.author:
            raise PermissionDenied
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['new_post_type'] = self.kwargs['post_type']
        return context


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, generic.DeleteView):
    model = Post
    template_name = 'news/delete.html'
    success_url = reverse_lazy('news:news_index')
    permission_required = ('news.change_post',)

    def get_object(self, **kwargs):
        obj = super().get_object(**kwargs)
        author = Author.objects.filter(user=self.request.user).first()
        if author != obj.author:
            raise PermissionDenied
        return obj

    def form_valid(self, form):
        if self.kwargs['post_type'] == 'AR':
            self.success_url = reverse_lazy('news:articles_index')
        return super().form_valid(form)


class Subscribe(LoginRequiredMixin, View):
    def get(self, request, category_id, **kwargs):
        category = Category.objects.filter(id=category_id).first()
        if category:
            category.subscribers.add(self.request.user)
            messages.add_message(request, messages.INFO, f'Succesfully subscribed to {category}!')
            next_url = request.GET.get('next', None)
            if next_url:
                return redirect(next_url)
            else:
                return redirect('pages:pages_index')
        else:
            return HttpResponse(f'Category with if: {category_id} not found')
