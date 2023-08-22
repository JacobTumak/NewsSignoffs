from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from article.models.models import Article


def redirect_to_home(request):
    return redirect('all_articles')


def custom_profile_redirect(request):
    user = request.user
    return redirect('user_profile', user.username)


def custom_logout(request):
    logout(request)
    return redirect('all_articles')


@login_required
def delete_article_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        article.delete()
        return redirect('my_articles')
    else:
        return render(request, 'article/delete_article.html', {'article': article})


@login_required
def my_articles_view(request):
    return article_list_base_view(request,
                                  page_title="My Articles",
                                  empty_text="You haven't written any articles yet.",
                                  author=request.user)


def all_articles_view(request):
    return article_list_base_view(request,
                                  page_title="All Articles",
                                  empty_text="Published articles will appear here.")


@login_required
def all_liked_articles_view(request):
    return article_list_base_view(request,
                                  page_title="Liked Articles",
                                  empty_text="Articles you like will appear here.",
                                  like_signatories__user=request.user)


def article_list_base_view(request, page_title=None, empty_text=None, **filter_kwargs):
    empty_text = empty_text or "Published articles will appear here."
    # filter_kwargs['is_published'] = True
    articles = Article.objects.filter(**filter_kwargs)
    context = {'articles': articles,
               'page_title': page_title,
               "empty_text": empty_text}
    return render(request, 'article/article_list_view.html', context=context)