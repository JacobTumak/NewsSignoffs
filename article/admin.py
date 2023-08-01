from django.contrib import admin
from article.models import TermsOfService, Article
from signoffs.contrib.signets.models import Signet, RevokedSignet

admin.site.register(TermsOfService)
admin.site.register(Article)

admin.site.register(Signet)
admin.site.register(RevokedSignet)
