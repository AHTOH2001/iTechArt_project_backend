from django.urls import path
from .views import LoginView, RefreshTokenView

urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('refresh_token/', RefreshTokenView.as_view())
]
