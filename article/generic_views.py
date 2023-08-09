from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from article.models.models import Article


def redirect_to_home(request):
    return redirect('all_articles')


def custom_profile_redirect(request):
    return redirect('my_articles')


def custom_logout(request):
    logout(request)
    return redirect('all_articles')


def delete_article_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        article.delete()
        return redirect('my_articles')
    else:
        return render(request, 'article/delete_article.html', {'article': article})


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
