from signoffs.contrib.signets.models import Signet
from signoffs.models import RevokedSignet, Signet
from django.db import models

# from article.models.models import Article


class PublicationRequestSignet(Signet):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='pub_request_signatories', editable=False)


class PublicationApprovalSignet(Signet):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='pub_approve_signatories', editable=False)


# class PublicationSignet(Signet):
#     article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='signatories', editable=False)

class RevokedNewsletterSignet(RevokedSignet):
    def __str__(self):
        return 'Revoked {type} by {user} at {time}'.format(type=self.signet.signoff.id,
                                                           user=self.user,
                                                           time=self.timestamp)


class ArticleSignet(Signet):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='signatories', editable=False)
