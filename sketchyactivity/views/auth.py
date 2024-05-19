import logging

from django.conf import settings
from django.contrib.auth import authenticate
from django.db import IntegrityError
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from sketchyactivity.serializers import UserSignUpSerializer

logger = logging.getLogger(__name__)

class LogoutView(APIView):
    def post(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@permission_classes([AllowAny])
class LoginView(APIView):
    def post(self, request, format=None):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            result = {
                "token": token.key,
                "username": user.username,
                "email": user.email,
            }
            return Response(result)
        else:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([AllowAny])
class SignUpView(APIView):
    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        logger.info(f"Serializer: {serializer}")
        if serializer.is_valid():
            # Create user
            try:
                user = serializer.save()
                user.set_password(request.data.get("password"))
                user.save()
                token, _ = Token.objects.get_or_create(user=user)
                result = {
                    "token": token.key,
                    "username": user.username,
                    "email": user.email,
                }
                return Response(result, status=status.HTTP_201_CREATED)
            except IntegrityError as e:
                logger.error(f"IntegrityError: {e}")
                return Response({"detail": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            logger.error(f"Serializer is not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)