from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, View

from .models import Newspaper, Topic
from newspaper_agency.forms import NewspaperForm


class HomePageView(ListView):
    """View class for the home page of the site."""
    model = Newspaper
    template_name = "newspaper_agency/newspaper_home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home page"
        return context

    def get_queryset(self):
        return Newspaper.objects.all().select_related("topic")


class GetNewspapersByTopic(ListView):
    """View class for the category page with newspapers with this topic."""
    model = Newspaper
    template_name = "newspaper_agency/topic.html"

    def get_queryset(self):
        return Newspaper.objects.filter(
            topic_id=self.kwargs["pk"]
        ).select_related("topic")


class NewspaperDetailView(DetailView):
    """View class for the newspaper detail page with commentaries."""
    model = Newspaper
    template_name = "newspaper_agency/newspaper_detail.html"
    context_object_name = "newspaper"


class CreateNewspaperView(LoginRequiredMixin, View):
    """View class for the page with creation form for the newspaper."""
    @staticmethod
    def get(request):
        form = NewspaperForm()
        return render(request, "newspaper_agency/create_newspaper.html", {"form": form})

    @staticmethod
    def post(request):
        form = NewspaperForm(request.POST)
        if form.is_valid():
            newspaper = form.save()
            return HttpResponseRedirect(reverse("newspaper-agency:newspaper-detail", kwargs={"pk": newspaper.pk}))
        return render(request, "newspaper_agency/create_newspaper.html", {"form": form})

    # model = Newspaper
    # fields = "__all__"
    # success_url = reverse_lazy("newspaper-agency:newspaper-detail")
