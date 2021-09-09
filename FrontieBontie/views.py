from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings

from .models import Profile
from .serializers import ProfileSerializer, ChangePasswordSerializer


class ProfileView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        return queryset.get(user=self.request.user)

    def patch(self, request, *args, **kwargs):
        try:
            response = super(ProfileView, self).patch(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        return response


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


@api_view(http_method_names=['PATCH'])
@permission_classes([IsAuthenticated])
def change_password_view(request):
    serializer = ChangePasswordSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
