from random import randint
from news.models import *

vasya = User.objects.create_user(username='vasya')
petya = User.objects.create_user(username='petya')

vasya_a = Author.objects.create(user=vasya)
petya_a = Author.objects.create(user=petya)


cat_world = Category.objects.create(title='World')
cat_tech = Category.objects.create(title='Tech')
cat_art = Category.objects.create(title='Art')
cat_humor = Category.objects.create(title='Humor')

p1 = Post.objects.create(author=vasya_a, title='Wow such news', content='much content', type='NW')
p2 = Post.objects.create(author=vasya_a, title='WTF is going on?', content='I truly dont understand what is happening in this part of world where i currently in nor what caused all this unspeakable events', type='AR')
p3 = Post.objects.create(author=petya_a, title='NVIDIA just announced RTX4070', content='lorem ipsum nvidia tuda syda', type='AR')
p4 = Post.objects.create(author=petya_a, title='Sculptor integrated AI into statue', content='There is a statue on the hill which have no eyes, but instead have fully self-aware AI that constantly saying stupid puns', type='AR')

p1.category.add(cat_world)
p2.category.add(cat_world, cat_humor)
p3.category.add(cat_tech)
p4.category.add(cat_tech, cat_art)

c1 = Comment.objects.create(author=petya, post=p1, text='first comment, yeah')
c2 = Comment.objects.create(author=vasya, post=p1, text='first comment!')
c3 = Comment.objects.create(author=petya, post=p1, text='lol nope')

c4 = Comment.objects.create(author=vasya, post=p2, text='@vasya you so smart, i always enjoing reading your posts')
c5 = Comment.objects.create(author=vasya, post=p2, text='how to delete comment')
c6 = Comment.objects.create(author=petya, post=p2, text='cringe')

c7 = Comment.objects.create(author=vasya, post=p3, text='Unbelievable')

c8 = Comment.objects.create(author=vasya, post=p4, text='hey @petya are you an AI too?')
c9 = Comment.objects.create(author=petya, post=p4, text='@vasya, who knows, hehe :P')

for post in Post.objects.all():
   post.like(randint(-10,10))

for comment in Comment.objects.all():
    comment.like(randint(-5,5))

vasya_a.update_rating()
petya_a.update_rating()

best_post = Post.objects.order_by('-rating').first()

print(best_post.timestamp, best_post.author.user.username, best_post.rating, best_post.title, best_post.preview())

for comment in best_post.comment_set.all():
    print(comment.timestamp, comment.author.username, comment.rating, comment.text)


