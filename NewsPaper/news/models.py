from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE, Sum
from django.db.models.functions import Coalesce


# Create your models here.
class Author(models.Model):
    full_name = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    rating = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=CASCADE)


    def update_rating(self):
        posts_rating = self.post_set.aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comments_rating = self.user.comment_set.aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        posts_comments_rating = self.post_set.aggregate(pcr=Coalesce(Sum('comment__rating'), 0))['pcr']

        print(posts_rating)
        print('----------')
        print(comments_rating)
        print('----------')
        print(posts_comments_rating)

        self.rating = posts_rating *3 + comments_rating + posts_comments_rating
        self.save()



class Category(models.Model):
    name_category = models.CharField(max_length=100, unique=True)


class Post(models.Model):
    article = "AR"
    news = "NW"
    POST_TYPE = [
        (article, "Статья"),
        (news, "Новости")
    ]

    author = models.ForeignKey(Author, on_delete=CASCADE)
    post_type = models.CharField(max_length=2, choices=POST_TYPE)
    create_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=255)
    text_post = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text_post[:124] + '...' if len(self.text_post) > 124 else self.text_post

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=CASCADE)
    category = models.ForeignKey(Category, on_delete=CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=CASCADE)
    comment = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()



