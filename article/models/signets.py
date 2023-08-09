from signoffs.models import RevokedSignet


class RevokedNewsletterSignet(RevokedSignet):
    def __str__(self):
        return 'Revoked {type} by {user} at {time}'.format(type=self.signet.signoff.id,
                                                           user=self.user,
                                                           time=self.timestamp)



