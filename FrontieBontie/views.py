from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Profile, Category
from .serializers import (ProfileSerializer, ChangePasswordSerializer, ProductSerializer, ResetPasswordSerializer,
                          CategorySerializer)


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


class AddProductView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data={**request.data, 'owner': request.user.pk})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def post(self, request, *args, **kwargs):
        try:
            response = super(AddProductView, self).post(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'detail': e.detail}, status=status.HTTP_400_BAD_REQUEST)
        return response


@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
def reset_password_view(request):
    serializer = ResetPasswordSerializer(request.user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CategoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
