from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = 0
        for post in self.post_set.all():
            self.rating += post.rating * 3
            for other_comment in post.comment_set.exclude(author__username=self.user.username):
                self.rating += other_comment.rating
        for comment in self.user.comment_set.all():
            self.rating += comment.rating
        self.save()

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return f'<Author id:{self.id} {self.user.username}#{self.user.id}>'


class Category(models.Model):
    title = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<Category #{self.id}: {self.title}>'


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
    timestamp = models.DateTimeField('Timestamp ', auto_now_add=True)
    rating = models.IntegerField(default=0)
    category = models.ManyToManyField(Category, through='PostCategory')

    def get_absolute_url(self):
        return reverse('news:news_detail', args=[str(self.id)])

    def preview(self):
        return self.content[:124] + '...'

    def like(self, amount=1):
        self.rating += amount
        self.save()

    def dislike(self):
        self.like(-1)

    def __str__(self):
        return f'{self.title} | {self.preview()}'

    def __repr__(self):
        return f'<Post #{self.id}>'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField('Timestamp ', auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self, amount=1):
        self.rating += amount
        self.save()

    def dislike(self):
        self.like(-1)

    def __str__(self):
        return f'{self.author}: {self.text}'

    def __repr__(self):
        return f'<Comment #{self.id} to {self.post!r}>'

