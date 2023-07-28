from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    article_text = models.TextField(max_length=1000, default='Article text goes here')
    article_images = models.ImageField(upload_to='images/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='article_likes')

