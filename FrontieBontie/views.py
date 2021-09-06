from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings


class ProfileView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        return Response({'username': user.username, 'email': user.email})


class LogOutView(CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        response = Response()
        response.delete_cookie(
            key=settings.COOKIE_APP['REFRESH_NAME'],
            path=settings.COOKIE_APP['PATH'],
            domain=settings.COOKIE_APP['DOMAIN'],
            samesite=settings.COOKIE_APP['SAMESITE'],
        )
        return response
