from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.PagesIndex.as_view(), name='pages_index'),
    path('accounts/profile/', views.AuthorProfile.as_view(), name='author_profile'),
    path('accounts/profile/upgrade/', views.upgrade_profile, name='author_profile_upgrade')
]
