from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from . import views

app_name = 'pages'
urlpatterns = [
    path('', views.PagesIndex.as_view(), name='pages_index'),
    # path('/')
]
