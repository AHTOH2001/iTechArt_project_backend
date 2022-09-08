from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from django.middleware import csrf
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import status
from django.utils import timezone


# https://www.procoding.org/jwt-token-as-httponly-cookie-in-django/
class LoginView(APIView):
    def post(self, request):
        data = request.data
        response = Response()
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                response.set_cookie(
                    key=settings.COOKIE_APP['REFRESH_NAME'],
                    value=str(refresh),
                    expires=timezone.localtime() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    secure=settings.COOKIE_APP['SECURE'],
                    httponly=settings.COOKIE_APP['HTTP_ONLY'],
                    samesite=settings.COOKIE_APP['SAMESITE']
                )
                csrf.get_token(request)
                response.data = {'access': str(refresh.access_token)}
                return response
            else:
                return Response({"detail": "This account is not active"}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({"detail": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class RefreshTokenView(APIView):
    def post(self, request):
        try:
            refresh = RefreshToken(request.COOKIES['refresh_token'])
        except KeyError:
            return Response({"detail": "Refresh token is missing"}, status=status.HTTP_401_UNAUTHORIZED)
        except TokenError as e:
            return Response({'detail': e.args[0]}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({'access': str(refresh.access_token)})
