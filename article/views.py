from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from article.models import Article #, Comment
from article.forms import ArticleForm, SignupForm


#################
# ARTICLE VIEWS #
#################


def redirect_to_home(request):
    return redirect('all_articles')


@login_required
def new_article_view(request):
    user = request.user

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        signoff_form = Article.publish_signoff.forms.get_signoff_form(request.POST)
        if form.is_valid():
            if signoff_form.is_signed_off():
                article = form.save(commit=False)
                article.author = user
                article.publish_signoff.sign(user)
                article.save()
                return redirect('article_detail', article.id)
            else:
                messages.error(request, "You must agree to the terms before publishing your article.")
    else:
        form = ArticleForm()

    return render(request, 'article/new_article.html', {'form': form, 'article': Article()})


@login_required()
def edit_article_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return render(request, 'article/article_detail.html', context={'article': article})
    else:
        form = ArticleForm(instance=article)
    return render(request, 'article/edit_article.html', {'form': form, 'article': article})


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


def custom_profile_redirect(request):
    return redirect('my_articles')


def custom_logout(request):
    logout(request)
    return redirect('all_articles')  # Replace 'home' with the URL name of your homepage view


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()  # Create new user

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            login(request, user)  # Login new user

            return redirect('all_articles')
    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {'form': form})


# @login_required
# def save_article_view(request, article_id):
#     article = get_object_or_404(Article, id=article_id)
#     if request.user in article.saves.all():
#         article.saves.remove(request.user)
#     else:
#         article.saves.add(request.user)
#     return HttpResponseRedirect(reverse('article_detail', args=[str(article_id)]))
