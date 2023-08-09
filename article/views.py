from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404, redirect
from django.urls import reverse

from signoffs.shortcuts import get_signoff_or_404, get_signet_or_404

from article.models import Article, Comment
from article.signoffs import terms_signoff, newsletter_signoff, comment_signoff
from article.forms import ArticleForm, CommentForm, SignupForm


def terms_check(user):
    signoff = terms_signoff.get(user=user)
    return signoff.is_signed()


@login_required
@user_passes_test(terms_check, login_url='terms_of_service')
def new_article_view(request):
    user = request.user

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        signoff_form = Article.publish_signoff.forms.get_signoff_form(request.POST)
        if form.is_valid() and signoff_form.is_valid():
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


@login_required
def edit_article_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect('article_detail', article.id)
    else:
        form = ArticleForm(instance=article)

    return render(request, 'article/edit_article.html', {'form': form, 'article': article})


def article_detail_view(request, article_id):
    user = request.user

    article = Article.objects.get(id=article_id)
    past_comments = Comment.objects.filter(article=article)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = user
            comment.article = article
            comment.comment_signoff.create(user)
            comment.save()
            return redirect('article_detail', article.id)
        else:
            messages.error(request, "You must agree to the terms before posting your comment.")
    else:
        form = CommentForm()

    context = {'article': article, 'form': form, 'past_comments': past_comments}
    return render(request, 'article/article_detail.html', context)


def revoke_comment_view(request, signet_id):
    comment = get_signet_or_404(comment_signoff, signet_id).comment
    comment.delete()
    return redirect(request.META.get('HTTP_REFERER', 'all_articles'))


@login_required
def like_article_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.user in article.likes.all():
        article.likes.remove(request.user)
    else:
        article.likes.add(request.user)
    return HttpResponseRedirect(reverse('article_detail', args=[str(article_id)]))


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()  # Create new user

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)

            login(request, user)  # Login new user

            return redirect('terms_of_service')

    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {'form': form})


def terms_of_service_view(request):
    user = request.user
    next_page = request.GET.get('next') or 'terms_of_service'

    signoff = terms_signoff.get(user=user)

    if request.method == 'POST':
        signoff_form = signoff.forms.get_signoff_form(request.POST)
        if signoff_form.is_signed_off():
            signoff.sign(user)
            return redirect(next_page)
        else:
            messages.error(request, "You must agree to the Terms of Service.")

    return render(request, 'registration/terms_of_service.html', {'signoff': signoff})


def newsletter_view(request):
    user = request.user

    signoff = newsletter_signoff.get(user=user)

    if request.method == 'POST':
        signoff_form = signoff.forms.get_signoff_form(request.POST)
        if signoff_form.is_signed_off():
            signoff.sign(user)
            return redirect('newsletter')
        else:
            messages.error(request, "You must check the box to sign up for our newsletter.")

    return render(request, 'registration/newsletter.html', {'signoff': signoff})


def revoke_newsletter_view(request, signet_id):
    signoff = get_signoff_or_404(newsletter_signoff, signet_id)
    signoff.revoke_if_permitted(user=request.user, reason='I no longer wish to receive the newsletter.')

    return redirect('newsletter')
