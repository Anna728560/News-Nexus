from django.urls import path

from .views import index, get_topic

urlpatterns = [
    path("", index, name="index"),
    path("topic/<int:pk>/", get_topic, name="get-topic-info")
]

app_name = "newspaper-agency"
