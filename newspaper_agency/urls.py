from django.urls import path

from .views import (
    get_topic,
    newspaper_detail,
    crete_newspaper, HomePageView
)

urlpatterns = [
    path("", HomePageView.as_view(), name="newspaper-home"),
    path("topic/<int:pk>/", get_topic, name="get-topic-info"),
    path("newspaper/<int:pk>/", newspaper_detail, name="newspaper-detail"),
    path("newspaper/create-newspaper/", crete_newspaper, name="create-newspaper"),
]

app_name = "newspaper-agency"
