from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = 0
        posts = self.post_set.all()
        for post in posts:
            self.rating += post.rating * 3
            for other_comment in post.comment_set.exclude(author__username=self.user.username):
                self.rating += other_comment.rating
        for comment in self.user.comment_set.all():
            self.rating += comment.rating
        self.save()


class Category(models.Model):
    title = models.CharField(max_length=64, unique=True)


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'

    TYPE_CHOICES = [
        (ARTICLE, 'Article'),
        (NEWS, 'News')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    content = models.TextField()
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default=ARTICLE)
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')

    def preview(self):
        return self.content[:124] + '...'

    def like(self, amount=1):
        self.rating += amount
        self.save()

    def dislike(self):
        self.like(-1)


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self, amount=1):
        self.rating += amount
        self.save()

    def dislike(self):
        self.like(-1)
