from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


# --- AUTH ---
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)


class RefreshTokenView(TokenRefreshView):
    permission_classes = [AllowAny]


# --- USERS ---
class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ["GET", "PATCH"]:
            return [IsAuthenticated()]
        elif self.request.method == "DELETE":
            return [IsAdminUser()]
        return super().get_permissions()

    def patch(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user != user and not request.user.is_staff:
            return Response({"detail": "Нет прав на изменение этого пользователя."}, status=403)
        return super().patch(request, *args, **kwargs)
