from django.db import models
from django.db.models import ForeignKey, CASCADE


class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField()


class Category(models.Model):
    name = models.CharField(max_length=50)


class Tag(models.Model):
    name = models.CharField(max_length=25)


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    author = ForeignKey(Author, on_delete=models.CASCADE)
    category = ForeignKey(Category, on_delete=models.CASCADE)
    tag = ForeignKey(Tag, on_delete=CASCADE)
