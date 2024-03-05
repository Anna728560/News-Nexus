from django import template

from newspaper_agency.models import Topic

register = template.Library()


@register.simple_tag()
def newspaper_tags():
    return Topic.objects.all()
