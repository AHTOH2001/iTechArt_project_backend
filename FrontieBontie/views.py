from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings

from .serializers import ProfileSerializer


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


class SignUpView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = ProfileSerializer

    def post(self, request, *args, **kwargs):
        try:
            response = super(SignUpView, self).post(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        return response
