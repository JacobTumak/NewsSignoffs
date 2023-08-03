from django import template
register = template.Library()

@register.inclusion_tag('tags/fact_check_badge.html')
def fact_check_badge(article):
    return {'article': article}
