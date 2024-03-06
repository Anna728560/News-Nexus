from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView

from .models import Newspaper, Topic
from newspaper_agency.forms import NewspaperForm


class HomePageView(ListView):
    """View class for the home page of the site."""
    model = Newspaper
    template_name = "newspaper_agency/newspaper_home.html"


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
    """View function for the page with creation form for the newspaper."""
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
