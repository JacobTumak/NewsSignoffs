from django.contrib import admin

from signoffs.contrib.signets.models import Signet, RevokedSignet

from article.models.models import Article
from article.models.signets import RevokedNewsletterSignet

# Signoffs Models

admin.site.register(Signet)
admin.site.register(RevokedSignet)


# Article Models

admin.site.register(Article)


@admin.register(RevokedNewsletterSignet)
class RevokedNewsletterSignetAdmin(admin.ModelAdmin):
    readonly_fields = ['signet', 'user', 'timestamp', 'reason']
