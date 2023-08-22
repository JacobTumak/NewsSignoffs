from signoffs.models import RevokedSignet, Signet
from django.db import models


class PublicationSignet(Signet):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, related_name='signatories', editable=False)
    pass

class RevokedNewsletterSignet(RevokedSignet):
    def __str__(self):
        return 'Revoked {type} by {user} at {time}'.format(type=self.signet.signoff.id,
                                                           user=self.user,
                                                           time=self.timestamp)



