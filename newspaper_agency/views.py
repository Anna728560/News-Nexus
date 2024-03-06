from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from .models import Newspaper, Topic
from newspaper_agency.forms import NewspaperForm


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


def crete_newspaper(request):
    if request.method == "POST":
        form = NewspaperForm(request.POST)
        if form.is_valid():
            newspaper = form.save()
            return HttpResponseRedirect(
                reverse(
                    "newspaper-agency:newspaper-detail",
                    kwargs={
                        "pk": newspaper.pk
                    }
                )
            )
    else:
        form = NewspaperForm()
    return render(request, "newspaper_agency/create_newspaper.html", context={"form": form})
