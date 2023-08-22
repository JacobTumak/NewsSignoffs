from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect, HttpResponseRedirect, reverse

from signoffs.shortcuts import get_signoff_or_404, get_signet_or_404

from article.models.models import Article, LikeSignet, Comment, comment_signoff
from article.generic_views import article_list_base_view
from article.signoffs import ArticlePublicationSignoffs as aps
from article.forms import ArticleForm, CommentForm, SignupForm


@login_required
def submit_for_publication(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    signoff = aps.publication_request_signoff(user=request.user)
    signoff_form = article.publication_request_signoff.forms.get_signoff_form(request.POST)
    if signoff_form.is_valid() and signoff_form.is_signed_off():
        signoff.sign(user=request.user)
        # return HttpResponseRedirect(reverse('article_detail', args=(article.id,)))


def approve_publication(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == "POST":
        signoff_form = Article.publication_approval_signoff.forms.get_signoff_form(request.POST)
        if signoff_form.is_valid() and signoff_form.is_signed_off():
            article.publication_approval_signoff.sign(request.user)
            # return HttpResponseRedirect(reverse('article_detail', args=(article.id,)))

@login_required
def pending_publication_requests(request):
    if not request.user.is_staff:
        messages.error(request, 'You must be a staff member to view the page you were trying to access')
        return redirect('all_articles')
    """Returns a queryset of pending publication requests."""

    # print(Article.publication_approval_signet.objects.filter(has_user=True))

    page_title = "Pending Publication Requests"
    empty_text = "There are no pending publication requests."
    return article_list_base_view(request,
                                  page_title,
                                  empty_text,
                                  publication_status='pending',)


