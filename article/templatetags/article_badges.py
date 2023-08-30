# This tag is not working at the moment, might re-purpose it and the corresponding html tag later


# from django import template
# from article.models import FactCheckSignet
# register = template.Library()
#
# @register.inclusion_tag('tags/fact_check_badge.html')
# def fact_check_badge(article):
#     style = "font-size: .75em;vertical-align: top;"
#     if FactCheckSignet.objects.filter(article=article).exists():
#         signet = FactCheckSignet.objects.get(article=article)
#         return {'result': signet.result ,
#                 'class': FactCheckSignet.BADGE_CFG[signet.result],
#                 'style': style}
#
#     return {'result': 'Not Fact Checked',
#             'class': FactCheckSignet.BADGE_CFG['not_fact_checked'],
#             'style': style}
