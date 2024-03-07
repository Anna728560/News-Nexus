from django import template
from django.db.models import Count

from newspaper_agency.models import Topic

register = template.Library()


@register.simple_tag()
def get_all_topics():
    return Topic.objects.all()


@register.inclusion_tag("newspaper_agency/topics_list.html")
def show_topics():
    topics = Topic.objects.annotate(cnt=Count("newspapers"))
    return {"topics": topics}
