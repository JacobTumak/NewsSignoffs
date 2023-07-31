from django.forms import ModelForm, Textarea, BooleanField
from signoffs.forms import AbstractSignoffForm
from article.models import Article #, Comment

class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'summary', 'article_text']
        widgets = {
            'summary': Textarea(attrs={'rows': 2}),  # Set the rows attribute to 2 for the summary field
        }


# class AgreeSignoffForm(AbstractSignoffForm):
#     """ Require the user to signoff for the form to validate """
#     signed_off = BooleanField(label='I agree', required=True)

# class CommentForm(ModelForm):
#     class Meta:
#         model = Comment
#         fields = ['comment_text']