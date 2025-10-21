from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
from .models import CustomUser


def send_verification_email(email, username):
    """SMTP orqali email yuborish funksiyasi"""
    sender = settings.EMAIL_ADDRESS
    password = settings.EMAIL_PASSWORD
    subject = "Welcome! Please verify your email"
    text = f"""
    Hello {username},

    Thank you for registering on our platform.
    Please verify your email to activate your account.

    Best regards,
    Your Team
    """

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = email
    msg["Subject"] = subject
    msg.attach(MIMEText(text, "plain"))

    try:
        with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.login(sender, password)
            server.send_message(msg)
        print(f"Verification email sent to {email}")
    except Exception as e:
        print(f"Email send error: {e}")


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("id", "email", "username", "first_name", "last_name", "password")

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            username=validated_data.get("username", validated_data["email"]),
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            password=validated_data["password"],
        )
        user.is_verified = False
        user.save()

        # Email yuborish
        send_verification_email(user.email, user.username)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError("Неверный email или пароль.")
        if not user.is_active:
            raise serializers.ValidationError("Аккаунт не активен.")
        if not user.is_verified:
            raise serializers.ValidationError("Email не верифицирован.")

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "email", "username", "first_name", "last_name", "is_verified", "is_staff")
