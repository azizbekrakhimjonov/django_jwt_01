from django.urls import path
from .views import (
    RegisterView, LoginView, RefreshTokenView,
    MeView, UserListView, UserDetailView
)

urlpatterns = [
    # AUTH
    path("auth/signup", RegisterView.as_view(), name="signup"),
    path("auth/login", LoginView.as_view(), name="login"),
    path("auth/refresh", RefreshTokenView.as_view(), name="token_refresh"),

    # USERS
    path("me", MeView.as_view(), name="me"),
    path("users", UserListView.as_view(), name="user_list"),
    path("users/<int:pk>", UserDetailView.as_view(), name="user_detail"),
]
