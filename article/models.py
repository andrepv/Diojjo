from django.db import models
from django.contrib.auth.models import User

from sorl.thumbnail import ImageField
from taggit.managers import TaggableManager
from geoposition.fields import GeopositionField


class Article(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=3000)
    author = models.ForeignKey(User)
    created_date = models.DateTimeField(auto_now_add=True)
    tags = TaggableManager()

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ("-created_date",)

    def get_likes(self):
        return Likes.objects.filter(article=self).count()

    def get_likers(self):
        likes = Likes.objects.filter(article=self.pk)
        likers = []
        for like in likes:
            likers.append(like.author)
        return likers

    def get_images(self):
        return Images.objects.filter(article=self)

    def get_comments(self):
        return Comment.objects.filter(article=self).order_by('-date')

    def location(self):
        return PointOfInterest.objects.filter(article=self)

    def __str__(self):
        return self.title


class Likes(models.Model):
    author = models.ForeignKey(User)
    article = models.ForeignKey(Article)


class Images(models.Model):
    article = models.ForeignKey(Article)
    image = ImageField(upload_to='article_images/%Y/%m/')


class Comment(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    comment = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Article Comment"
        verbose_name_plural = "Article Comments"
        ordering = ("date",)

    def __str__(self):
        return '{0} - {1}'.format(self.user.username, self.article.title)


class PointOfInterest(models.Model):
    article = models.ForeignKey(Article)
    position = GeopositionField()
