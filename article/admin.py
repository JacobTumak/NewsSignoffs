from django.contrib import admin

from signoffs.contrib.signets.models import Signet, RevokedSignet

from article.models.models import Article
from article.models.signets import RevokedNewsletterSignet


admin.site.register(Article)

admin.site.register(Signet)
admin.site.register(RevokedSignet)
admin.site.register(RevokedNewsletterSignet)
