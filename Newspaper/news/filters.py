from django_filters import FilterSet
from .models import Post


class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'rating': ['gt', 'lt'],
            'timestamp': ['gt']
        }


class PostCategoryFilter(FilterSet):
    class Meta:
        model = Post
        fields = ['category']
