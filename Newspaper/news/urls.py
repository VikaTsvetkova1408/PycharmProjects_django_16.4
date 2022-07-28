from django.urls import path, include

from . import views

app_name = 'news'

news_patterns = [
    path('news/', views.IndexView.as_view(), name='news_index'),
    path('news/create/', views.PostCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit', views.PostEdit.as_view(), name='news_edit'),
    path('news/<int:pk>/delete', views.PostDelete.as_view(), name='news_delete'),
]

articles_patterns = [
    path('articles/', views.IndexView.as_view(), name='articles_index'),
    path('articles/create/', views.PostCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit', views.PostEdit.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete', views.PostDelete.as_view(), name='articles_delete'),
]

urlpatterns = [
    path('post/<int:pk>', views.DetailView.as_view(), name='post_detail'),
    path('', include(news_patterns), {'post_type': 'NW'}),
    path('', include(articles_patterns), {'post_type': 'AR'}),
    path('search/', views.SearchView.as_view(), name='posts_search'),
]
