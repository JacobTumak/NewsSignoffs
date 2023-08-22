from django.forms import ModelForm, TextInput, Textarea
from django.contrib.auth.forms import UserCreationForm
from article.models.models import Article, Comment


class SignupForm(UserCreationForm):
    pass


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        readonly_fields = ['publication_status', 'author']
        fields = ['title', 'summary', 'article_text']
        widgets = {
            'title': TextInput(attrs={'style': 'width:100%'}),
            'summary': Textarea(attrs={'rows': 2, 'style': 'width:100%'}),  # Set the rows attribute to 2 for the summary field
            'article_text': Textarea(attrs={'rows': 10, 'style': 'width:100%'}),
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']
        widgets = {
            'comment_text': Textarea(attrs={'rows': 5,
                                            'class': 'rounded border-light p-3',
                                            'style': 'width:100%',
                                            'placeholder': 'Share your thoughts...'}),
        }
