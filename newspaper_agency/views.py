from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View, UpdateView

from .forms import (
    RedactorCreationForm,
    RedactorLoginForm,
    NewspaperSearchForm,
    CreateCommentaryForm,
    NewspaperForm,
)
from .models import Newspaper, Topic


class HomePageView(ListView):
    """View class for the home page of the site."""

    model = Newspaper
    template_name = "newspaper_agency/newspaper_home.html"
    paginate_by = 10
    queryset = Newspaper.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home page"
        context["search_form"] = NewspaperSearchForm()
        context["topics"] = Topic.objects.all()
        return context

    def get_queryset(self):
        title = self.request.GET.get("title")
        if title:
            return self.model.objects.filter(title__icontains=title)

        return self.queryset


class GetNewspapersByTopic(ListView):
    """View class for the category page with newspapers with this topic."""

    model = Newspaper
    template_name = "newspaper_agency/topic.html"
    paginate_by = 10

    def get_queryset(self):
        return Newspaper.objects.filter(topic_id=self.kwargs["pk"]).select_related(
            "topic"
        )


class NewspaperDetailView(DetailView):
    """View class for the newspaper detail page with commentaries."""

    model = Newspaper
    template_name = "newspaper_agency/newspaper_detail.html"
    context_object_name = "newspaper"


class CreateNewspaperView(LoginRequiredMixin, CreateView):
    """View class for the page with creation form for the newspaper."""

    model = Newspaper
    form_class = NewspaperForm

    def form_valid(self, form):
        newspaper = form.save(commit=False)
        newspaper.save()
        newspaper.publishers.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "newspaper-agency:newspaper-detail", kwargs={"pk": self.object.pk}
        )


class UpdateNewspaperView(LoginRequiredMixin, UpdateView):
    """View class for the page with update form for the newspaper."""
    model = Newspaper
    form_class = NewspaperForm

    def get_success_url(self):
        return reverse_lazy(
            "newspaper-agency:newspaper-detail", kwargs={"pk": self.object.pk}
        )


class UserRegisterView(View):
    """View class for the page with registration."""

    def get(self, request):
        form = RedactorCreationForm()
        return render(request, "newspaper_agency/register.html", {"form": form})

    def post(self, request):
        form = RedactorCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("newspaper_agency:login")

        return render(request, "newspaper_agency/register.html", {"form": form})


class UserLoginView(View):
    """View class for the page with login."""

    def get(self, request):
        form = RedactorLoginForm()
        return render(request, "newspaper_agency/login.html", {"form": form})

    def post(self, request):
        form = RedactorLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("newspaper-agency:newspaper-home")

        return render(request, "newspaper_agency/login.html", {"form": form})


class UserLogoutView(View):
    """View class for the page with logout."""

    def get(self, request):
        logout(request)
        return redirect("newspaper-agency:login")


class CreateCommentView(LoginRequiredMixin, View):
    """View class for the creation comment."""

    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect("newspaper-agency:login")
        newspaper = get_object_or_404(Newspaper.objects.prefetch_related("publishers"), pk=pk)
        form = CreateCommentaryForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.newspaper = newspaper
            comment.save()
            return redirect("newspaper-agency:newspaper-detail", pk=pk)

        return redirect("newspaper-agency:newspaper-detail", pk=pk)


@login_required
def add_of_remove_editor_to_authors(request, pk):
    """Function that allows to add or remove redactors name to/from editors."""
    newspaper = get_object_or_404(Newspaper, pk=pk)
    if request.user in newspaper.publishers.all():
        newspaper.publishers.remove(request.user)
    else:
        newspaper.publishers.add(request.user)
    return redirect("newspaper-agency:newspaper-detail", pk=newspaper.pk)


@login_required
def remove_newspaper(request, pk):
    """Function that allows to remove newspaper if redactor is in editors."""
    newspaper = get_object_or_404(Newspaper, pk=pk)
    if request.user in newspaper.publishers.all():
        newspaper.delete()
    return redirect("newspaper-agency:newspaper-home")
