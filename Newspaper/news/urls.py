from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='news_index'),
    path('news/', views.news_list, name='news_list'),
    path('news/<int:news_id>', views.news_details, name='news_details'),
]
