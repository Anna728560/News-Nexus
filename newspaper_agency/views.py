from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from .models import Newspaper, Topic


@login_required
def index(request):
    """View function for the home page of the site."""

    newspaper_list = Newspaper.objects.all().select_related("topic")
    context = {
        'newspaper_list': newspaper_list,
    }
    return render(request, "newspaper_agency/index.html", context=context)


def get_topic(request, pk):
    """View function for the category page with newspapers with this topic."""
    topic = Topic.objects.get(id=pk)
    newspaper_list = Newspaper.objects.filter(topic_id=pk)

    context = {
        "newspaper_list": newspaper_list,
        "topic": topic,
    }

    return render(request, "newspaper_agency/topic.html", context=context)


def newspaper_detail(request, pk):
    """View function for the newspaper detail page with commentaries."""
    newspaper = get_object_or_404(Newspaper, id=pk)
    context = {
        "newspaper": newspaper
    }
    return render(request, "newspaper_agency/newspaper_detail.html", context=context)