from django.db import models
from signoffs.models import Signet, RevokedSignet
from article.models import Comment


class RevokedNewsletterSignet(RevokedSignet):
    def __str__(self):
        return 'Revoked {type} by {user} at {time}'.format(type=self.signet.signoff.id,
                                                           user=self.user,
                                                           time=self.timestamp)


class CommentSignet(Signet):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='signatories')

