
# Before trying to fix "type object 'LikeSignoff' has no attribute 'objects'"
@login_required
def like_article_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    like_signoff_instance, created = like_signoff.objects.get_or_create(user_id=request.user.id, article_id=article.id)
    if not created and like_signoff_instance.can_revoke(user=request.user):
        # implies that the user has already liked the article
        like_signoff_instance.revoke(user=request.user, reason='Unlike Article')
        like_signoff_instance.save()
    else:
        like_signoff_instance.sign(request.user)
        like_signoff_instance.article = article
        like_signoff_instance.save()
    return HttpResponseRedirect(reverse('article_detail', args=[str(article_id)]))