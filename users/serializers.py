from rest_framework import serializers
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email"]


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = CustomUser.objects.filter(username=data["username"]).first()
        if user and user.check_password(data["password"]):
            refresh = RefreshToken.for_user(user)
            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        raise serializers.ValidationError("Invalid credentials")
