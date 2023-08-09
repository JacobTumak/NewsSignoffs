
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.urls import reverse
from article.models.models import Article


def redirect_to_home(request):
    return redirect('all_articles')

def custom_profile_redirect(request):
    return redirect('my_articles')


def custom_logout(request):
    logout(request)
    return redirect('all_articles')


def article_detail_view(request, article_id):
    article = Article.objects.get(id=article_id)
    return render(request, 'article/article_detail.html', {'article': article})


def delete_article_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    article.delete()
    return HttpResponseRedirect(reverse('my_articles'))


@login_required
def my_articles_view(request):
    articles = Article.objects.all().filter(author=request.user)
    context = {'articles': articles,
               'page_title': 'My Articles',
               "empty_text": "You haven't written any articles yet."}
    return render(request, 'article/article_list_view.html', context=context)


def all_articles_view(request):
    articles = Article.objects.all()
    context = {'articles': articles,
               'page_title': 'All Articles',
               "empty_text": "Published articles will appear here."}
    return render(request, 'article/article_list_view.html', context=context)


@login_required
def all_liked_articles_view(request):
    articles = Article.objects.all().filter(likes=request.user)
    context = {'articles': articles,
               'page_title': 'Liked Articles',
               "empty_text": "Articles you like will appear here."}
    return render(request, 'article/article_list_view.html', context=context)