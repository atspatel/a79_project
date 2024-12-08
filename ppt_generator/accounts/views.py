# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import permissions


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            raise AuthenticationFailed("Email and password are required")

        user = authenticate(request, username=email, password=password)

        if user is None:
            raise AuthenticationFailed("Invalid credentials")

        # Create JWT token
        refresh = RefreshToken.for_user(user)
        return Response({"refresh": str(refresh), "access": str(refresh.access_token)})


class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Ensure user is authenticated

    def get(self, request):
        # Return the email of the authenticated user
        return Response({"email": request.user.email})
