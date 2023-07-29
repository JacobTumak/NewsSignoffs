from django.forms import forms, ModelForm, Textarea
from article.models import Article, Comment

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'summary', 'article_text']
        widgets = {
            'summary': Textarea(attrs={'rows': 2}),  # Set the rows attribute to 2 for the summary field
        }

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']