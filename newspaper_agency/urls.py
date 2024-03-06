from django.urls import path

from .views import (
    index,
    get_topic,
    newspaper_detail,
    crete_newspaper
)

urlpatterns = [
    path("", index, name="index"),
    path("topic/<int:pk>/", get_topic, name="get-topic-info"),
    path("newspaper/<int:pk>/", newspaper_detail, name="newspaper-detail"),
    path("newspaper/create-newspaper/", crete_newspaper, name="create-newspaper"),
]

app_name = "newspaper-agency"
