from django.contrib import admin
from article.models import Article
from signoffs.contrib.signets.models import Signet, RevokedSignet

admin.site.register(Article)

admin.site.register(Signet)
admin.site.register(RevokedSignet)
