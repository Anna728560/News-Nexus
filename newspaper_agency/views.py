from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View

from .forms import (
    RedactorCreationForm,
    RedactorLoginForm,
    TopicSearchForm,
    CreateCommentaryForm,
    NewspaperForm,
)
from .models import Newspaper, Topic


class HomePageView(ListView):
    """View class for the home page of the site."""

    model = Newspaper
    template_name = "newspaper_agency/newspaper_home.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home page"
        context["search_form"] = TopicSearchForm()
        context["topics"] = Topic.objects.all()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        topic_id = self.request.GET.get("topic")
        if topic_id:
            topic = get_object_or_404(Topic, pk=topic_id)
            queryset = queryset.filter(topic=topic)
        return queryset.select_related("topic")


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
    template_name = "newspaper_agency/create_newspaper.html"

    def get_success_url(self):
        return reverse_lazy(
            "newspaper-agency:newspaper-detail", kwargs={"pk": self.object.pk}
        )


class UserRegisterView(View):
    def get(self, request):
        form = RedactorCreationForm()
        return render(request, "newspaper_agency/register.html", {"form": form})

    def post(self, request):
        form = RedactorCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("newspaper_agency:login")
        else:
            return render(request, "newspaper_agency/register.html", {"form": form})


class UserLoginView(View):
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
    def get(self, request):
        logout(request)
        return redirect("newspaper-agency:login")


class CreateCommentView(LoginRequiredMixin, View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect("newspaper-agency:login")
        newspaper = get_object_or_404(Newspaper, pk=pk)
        form = CreateCommentaryForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.newspaper = newspaper
            comment.save()
            return redirect("newspaper-agency:newspaper-detail", pk=pk)
        else:
            return redirect("newspaper-agency:newspaper-detail", pk=pk)
