from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    HttpResponseRedirect,
)
from django.urls import reverse

from signoffs.shortcuts import get_signoff_or_404, get_signet_or_404

from article.generic_views import article_list_base_view
from article.models.models import Article, Comment, comment_signoff
from article.models.signets import ArticleSignet, LikeSignet
from article.signoffs import (
    terms_signoff,
    newsletter_signoff,
    publication_request_signoff,
    publication_approval_signoff,)
from article.forms import ArticleForm, CommentForm, SignupForm


def terms_check(user):
    signoff = terms_signoff.get(user=user)
    return signoff.is_signed()


@login_required
def request_publication_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    signoff_form = article.publication_request_signoff.forms.get_signoff_form(
        request.POST
    )
    if signoff_form.is_valid() and signoff_form.is_signed_off():
        signoff = signoff_form.sign(user=request.user, commit=False)
        signoff.signet.article = article
        signoff.save()
    return HttpResponseRedirect(reverse("article_detail", args=(article.id,)))


def revoke_publication_request_view(request, signet_pk):
    signet = get_signet_or_404(publication_request_signoff, signet_pk)
    signoff = signet.get_signoff()
    article = signet.article
    signoff.revoke_if_permitted(request.user, signet=signet)

    approval_signoff = publication_approval_signoff.get(
        article=article,
    )
    if approval_signoff.has_user():
        approval_signoff.revoke_if_permitted(
            request.user, reason="Publication Request Revoked"
        )

    return HttpResponseRedirect(reverse("article_detail", args=(article.id,)))


@login_required
def approve_publication_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if not request.user.is_staff or request.user == article.author:
        messages.error( request, "You do not have permission to approve this article for publication.",)
        return HttpResponseRedirect(reverse("article_detail", args=(article.id,)))

    signoff_form = article.publication_approval_signoff.forms.get_signoff_form(request.POST)

    if signoff_form.is_valid() and signoff_form.is_signed_off():
        signoff = signoff_form.sign(user=request.user, commit=False)
        signoff.signet.article = article
        signoff.save()
    return HttpResponseRedirect(reverse("article_detail", args=(article.id,)))

@login_required
def revoke_publication_approval_view(request, signet_pk):
    signet = get_object_or_404(ArticleSignet, id=signet_pk)
    signoff = signet.get_signoff()
    article = signet.article
    signoff.revoke_if_permitted(request.user)
    signet.delete()
    return HttpResponseRedirect(reverse("article_detail", args=(article.id,)))


@login_required
def pending_publication_requests(request):
    """Returns a queryset of pending publication requests."""
    if not request.user.is_staff:
        messages.error(
            request,
            "You must be a staff member to view the page you were trying to access",
        )
        return redirect("all_articles")
    # print(Article.publication_approval_signet.objects.filter(has_user=True))

    page_title = "Pending Publication Requests"
    empty_text = "There are no pending publication requests."
    return article_list_base_view(request, page_title, empty_text, publication_status="pending")


@login_required
@user_passes_test(terms_check, login_url="terms_of_service")
def new_article_view(request):
    signoff = publication_request_signoff
    user = request.user
    if request.method == "POST":
        print(request.POST)
        form = ArticleForm(request.POST)
        if form.is_valid():
            draft = form.save(commit=False)
            draft.author = user
            draft.save()
            if request.POST.get("signed_off") == "on":
                return request_publication_view(request, draft.id)
            return redirect("article_detail", draft.id)
    else:
        form = ArticleForm()
    context = {"form": form, "article": Article(), "signoff": signoff()}
    return render(request, "article/new_article.html", context=context)


@login_required
def edit_article_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)

    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect("article_detail", article.id)
    else:
        form = ArticleForm(instance=article)

    return render(
        request, "article/edit_article.html", {"form": form, "article": article}
    )


def article_detail_view(request, article_id):
    user = request.user

    article = Article.objects.get(id=article_id)
    article.update_publication_status()
    has_liked = article.likes.has_signed(user=user)
    comments = Comment.objects.filter(article=article)

    if request.method == "POST":
        if request.POST.get("signoff_id") == publication_request_signoff.id:
            return request_publication_view(request, article.id)
        elif request.POST.get("signoff_id") == publication_approval_signoff.id:
            return approve_publication_view(request, article.id)

    if article.publication_request_signoff.has_signed(article.author):
        pr_signoff = article.signatories.get(
            user=article.author, article=article
        ).get_signoff()
    else:
        pr_signoff = publication_request_signoff

    pa_signoff = publication_approval_signoff.get(
        article=article, signoff_id="publication_approval_signoff"
    )

    if not pa_signoff.is_signed():
        pa_signoff = publication_approval_signoff

    context = {
        "article": article,
        "form": CommentForm(),
        "user_has_liked": has_liked,
        "comments": comments,
        "publication_request_signoff": pr_signoff,
        "publication_approval_signoff": pa_signoff,
    }
    return render(request, "article/article_detail.html", context)


def add_comment(request, article_id):
    print(request.POST)
    user = request.user
    article = get_object_or_404(Article, id=article_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = user
            comment.article = article
            comment.comment_signoff.create(user)
            comment.save()
            return HttpResponseRedirect(reverse("article_detail", args=(article.id,)))
        else:
            messages.error(
                request, "You must agree to the terms before posting your comment."
            )


@login_required
def revoke_comment_view(request, signet_pk):
    comment = get_signet_or_404(comment_signoff, signet_pk).comment
    comment.delete()
    return redirect(request.META.get("HTTP_REFERER", "all_articles"))


@login_required
def like_article_view(request, article_id):
    user = request.user
    article = get_object_or_404(Article, id=article_id)

    if article.likes.has_signed(user=user):
        like = LikeSignet.objects.get(
            signoff_id="like_signoff", article=article, user=user
        ).signoff
        like.revoke_if_permitted(user=user)
    else:
        article.likes.create(user=user)

    return redirect("article_detail", article.id)


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()  # Create new user

            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)

            login(request, user)  # Login new user

            return redirect("terms_of_service")

    else:
        form = SignupForm()

    return render(request, "registration/signup.html", {"form": form})


@login_required
def user_profile_view(request, username):
    user = request.user
    terms_so = terms_signoff.get(user=user)
    newsletter_so = newsletter_signoff.get(user=user)
    verified_so = None

    drafts = Article.objects.filter(author=user, publication_status="not_requested")
    my_articles = Article.objects.filter(author=user, publication_status="pending")
    my_published_articles = Article.objects.filter(
        author=user, publication_status="published"
    )
    liked_articles = Article.objects.filter(like_signatories__user=user)

    context = {
        "terms_so": terms_so,
        "newsletter_so": newsletter_so,
        "verified_so": verified_so,
        "drafts": drafts,
        "my_articles": my_articles,
        "my_published_articles": my_published_articles,
        "liked_articles": liked_articles,
    }
    return render(request, "registration/user_profile.html", context)


@login_required
def terms_of_service_view(request):
    user = request.user
    next_page = request.GET.get("next") or ("user_profile", user.username)

    signoff = terms_signoff.get(user=user)

    if request.method == "POST":
        signoff_form = signoff.forms.get_signoff_form(request.POST)
        if signoff_form.is_signed_off():
            signoff.sign(user)
            return redirect(*next_page)
        else:
            messages.error(request, "You must agree to the Terms of Service.")

    return render(request, "registration/terms_of_service.html", {"signoff": signoff})


@login_required
def newsletter_view(request):
    user = request.user

    signoff = newsletter_signoff.get(user=user)

    if request.method == "POST":
        signoff_form = signoff.forms.get_signoff_form(request.POST)
        if signoff_form.is_signed_off():
            signoff.sign(user)
            return redirect("newsletter")
        else:
            messages.error(request, "You must check the box to sign up for our newsletter.")

    return render(request, "registration/newsletter.html", {"signoff": signoff})


@login_required
def revoke_newsletter_view(request, signet_pk):
    signoff = get_signoff_or_404(newsletter_signoff, signet_pk)
    signoff.revoke_if_permitted(
        user=request.user, reason="I no longer wish to receive the newsletter."
    )

    return redirect(request.META.get("HTTP_REFERER", "newsletter"))
