from django.urls import path
from users.views import RegisterView, LoginView, UserDetailView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
