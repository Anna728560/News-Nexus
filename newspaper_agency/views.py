from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, View

from .forms import RedactorCreationForm, RedactorLoginForm
from .models import Newspaper


class HomePageView(ListView):
    """View class for the home page of the site."""
    model = Newspaper
    template_name = "newspaper_agency/newspaper_home.html"
    paginate_by = 5

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
    paginate_by = 5

    def get_queryset(self):
        return Newspaper.objects.filter(
            topic_id=self.kwargs["pk"]
        ).select_related("topic")


class NewspaperDetailView(DetailView):
    """View class for the newspaper detail page with commentaries."""
    model = Newspaper
    template_name = "newspaper_agency/newspaper_detail.html"
    context_object_name = "newspaper"


class CreateNewspaperView(LoginRequiredMixin, CreateView):
    """View class for the page with creation form for the newspaper."""
    model = Newspaper
    fields = "__all__"
    template_name = "newspaper_agency/create_newspaper.html"

    def get_success_url(self):
        return reverse_lazy(
            "newspaper-agency:newspaper-detail",
            kwargs={"pk": self.object.pk}
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
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("newspaper-agency:newspaper-home")
        return render(request, "newspaper_agency/login.html", {"form": form})


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("newspaper-agency:login")
