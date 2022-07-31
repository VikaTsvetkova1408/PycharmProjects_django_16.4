from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from news.models import Author


class PagesIndex(TemplateView):
    template_name = 'pages/index.html'


class AuthorProfile(LoginRequiredMixin, TemplateView):
    template_name = 'pages/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(name='authors').exists()
        return context


@login_required
def upgrade_profile(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)

    author = Author.objects.filter(user=user).first()
    if not author:
        Author.objects.create(user=user)

    return redirect('pages:author_profile')

#
# def pages_index(request):
#     return render(request, 'pages/index.html')
#
#
