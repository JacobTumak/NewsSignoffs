from django.db import models
from django.contrib.auth.models import User

from signoffs.models import SignoffField, ApprovalField

from article.signoffs import publish_article_signoff
from article.approvals import publication_request_signoff, publication_approval_signoff


class Article(models.Model):
    title = models.CharField(max_length=200,)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='article_author')
    summary = models.TextField(max_length=100, null=False, blank=False)
    article_text = models.TextField(max_length=1000,)
    likes = models.ManyToManyField(User, related_name='article_likes')

    publish_signoff, publish_signet = SignoffField(publish_article_signoff)

    def __str__(self):
        if self.author.get_full_name() != "":
            return f"{self.author.get_full_name()} - {self.title}"
        else:
            return f"{self.author.username} - {self.title}"

    def delete(self, *args, **kwargs):
        self.publish_signet.delete()     # Delete the signet associated with the article
        super().delete(*args, **kwargs)  # Delete the article itself

    def total_likes(self):
        return self.likes.count()

    def is_author(self, user=None, username=None):
        if user==None and username==None:
            raise ValueError("Either user or username must be provided")
        return self.author == user or self.author.username == username

    def get_author_name(self):
        if self.author.get_full_name() != "":
            return self.author.get_full_name()
        else:
            return self.author.username
