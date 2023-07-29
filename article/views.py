from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from article.models import Article, Comment
from article.forms import ArticleForm

#################
# ARTICLE VIEWS #
#################

@login_required
def new_article_view(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return render(request, 'article/article_detail.html', context={'article': article})
    form = ArticleForm()
    return render(request, 'article/new_article.html', {'form': form})

def article_detail_view(request, article_id):
    article = Article.objects.get(id=article_id)
    return render(request, 'article/article_detail.html', {'article': article})

@login_required
def my_articles_view(request):
    articles = Article.objects.all().filter(author=request.user)
    return render(request, 'article/my_articles.html', {'articles': articles})

def all_articles_view(request):
    articles = Article.objects.all()
    return render(request, 'article/all_articles.html', {'articles': articles})

@login_required
def all_liked_articles_view(request):
    articles = Article.objects.all().filter(likes=request.user)
    return render(request, 'article/liked_articles.html', {'articles': articles})

@login_required
def like_article_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.user in article.likes.all():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    return HttpResponseRedirect(reverse('article_detail', args=[str(article_id)]))

# @login_required
# def save_article_view(request, article_id):
#     article = get_object_or_404(Article, id=article_id)
#     if request.user in article.saves.all():
#         article.saves.remove(request.user)
#     else:
#         article.saves.add(request.user)
#     return HttpResponseRedirect(reverse('article_detail', args=[str(article_id)]))
