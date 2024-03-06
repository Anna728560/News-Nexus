from django.urls import path

from .views import index, get_topic, newspaper_detail

urlpatterns = [
    path("", index, name="index"),
    path("topic/<int:pk>/", get_topic, name="get-topic-info"),
    path("newspaper/<int:pk>/", newspaper_detail, name="newspaper-detail"),
]

app_name = "newspaper-agency"
