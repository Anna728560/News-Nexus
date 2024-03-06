from django.urls import path

from .views import (
    HomePageView,
    GetNewspapersByTopic,
    NewspaperDetailView,
    CreateNewspaperView
)

urlpatterns = [
    path("", HomePageView.as_view(), name="newspaper-home"),
    path("topic/<int:pk>/", GetNewspapersByTopic.as_view(), name="get-topic-info"),
    path("newspaper/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspaper/create-newspaper/", CreateNewspaperView.as_view(), name="create-newspaper"),
]

app_name = "newspaper-agency"
