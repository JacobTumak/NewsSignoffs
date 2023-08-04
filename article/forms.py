from django.forms import ModelForm, TextInput, Textarea
from django.contrib.auth.forms import UserCreationForm
from article.models.models import Article


class SignupForm(UserCreationForm):
    pass


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'summary', 'article_text']
        widgets = {
            'title': TextInput(attrs={'style': 'width:100%'}),
            'summary': Textarea(attrs={'rows': 2, 'style': 'width:100%'}),  # Set the rows attribute to 2 for the summary field
            'article_text': Textarea(attrs={'rows': 10, 'style': 'width:100%'}),
        }
