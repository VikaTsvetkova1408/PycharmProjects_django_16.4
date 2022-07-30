from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class PagesIndex(TemplateView):
    template_name = 'pages/index.html'


class AuthorProfile(TemplateView):
    template_name = 'pages/profile.html'

#
# def pages_index(request):
#     return render(request, 'pages/index.html')
#
#
