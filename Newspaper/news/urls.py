from django.urls import path

from . import views

app_name = 'news'
urlpatterns = [
    path('news/', views.IndexView.as_view(), {'post_type': 'NW'}, name='news_index'),
    path('news/<int:pk>', views.DetailView.as_view(), {'post_type': 'NW'}, name='news_detail'),
    path('news/create/', views.PostCreate.as_view(), {'post_type': 'NW'}, name='news_create'),
    path('news/edit/', views.PostCreate.as_view(), {'post_type': 'NW'}, name='news_edit'),
    path('news/delete/<int:pk>', views.PostCreate.as_view(), {'post_type': 'NW'}, name='news_delete'),

    path('search/', views.SearchView.as_view(), name='news_search'),

    path('articles/', views.IndexView.as_view(), {'post_type': 'AR'}, name='articles_index'),
    path('articles/create/', views.PostCreate.as_view(), {'post_type': 'AR'}, name='articles_create'),
    path('articles/edit/', views.PostCreate.as_view(), {'post_type': 'AR'}, name='articles_edit'),
    path('articles/delete/<int:pk>', views.PostCreate.as_view(), {'post_type': 'AR'}, name='articles_delete'),

]
