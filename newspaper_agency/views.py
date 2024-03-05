from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Newspaper


@login_required
def index(request):
    """View function for the home page of the site."""

    newspaper_list = Newspaper.objects.all().select_related("topic")
    context = {
        'newspaper_list': newspaper_list,
    }
    return render(request, "newspaper_agency/index.html", context=context)
