from django.urls import path

from .views import (
    HomePageView,
    GetNewspapersByTopic,
    NewspaperDetailView,
    CreateNewspaperView,
    UserRegisterView,
    UserLoginView,
    UserLogoutView,
    CreateCommentView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("", HomePageView.as_view(), name="newspaper-home"),
    path("topic/<int:pk>/", GetNewspapersByTopic.as_view(), name="get-topic-info"),
    path("newspaper/<int:pk>/", NewspaperDetailView.as_view(), name="newspaper-detail"),
    path("newspaper/create-newspaper/", CreateNewspaperView.as_view(), name="create-newspaper"),
    path("<int:pk>/create-comment", CreateCommentView.as_view(), name="create-comment"),
]

app_name = "newspaper_agency"
