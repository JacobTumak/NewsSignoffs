from django.forms import ModelForm, TextInput, Textarea, BooleanField
from django.contrib.auth.forms import UserCreationForm
from signoffs.forms import AbstractSignoffForm
from article.models import Article #, Comment


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


# class AgreeSignoffForm(AbstractSignoffForm):
#     """ Require the user to signoff for the form to validate """
#     signed_off = BooleanField(label='I agree', required=True)

# class CommentForm(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['comment_text']