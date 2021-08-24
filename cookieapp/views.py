from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import status
from datetime import timedelta


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(APIView):
    def post(self, request):
        data = request.data
        response = Response()
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key=settings.COOKIE_APP['AUTH_COOKIE'],
                    value=data["access"],
                    expires=timedelta(minutes=5),
                    secure=settings.COOKIE_APP['AUTH_COOKIE_SECURE'],
                    httponly=settings.COOKIE_APP['AUTH_COOKIE_HTTP_ONLY'],
                    samesite=settings.COOKIE_APP['AUTH_COOKIE_SAMESITE']
                )
                csrf.get_token(request)
                response.data = data
                return response
            else:
                return Response({"detail": "This account is not active"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
