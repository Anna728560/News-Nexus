from django.urls import path

from .views import (
    HomePageView,
    GetNewspapersByTopic,
    newspaper_detail,
    crete_newspaper,
)

urlpatterns = [
    path("", HomePageView.as_view(), name="newspaper-home"),
    path("topic/<int:pk>/", GetNewspapersByTopic.as_view(), name="get-topic-info"),
    path("newspaper/<int:pk>/", newspaper_detail, name="newspaper-detail"),
    path("newspaper/create-newspaper/", crete_newspaper, name="create-newspaper"),
]

app_name = "newspaper-agency"
