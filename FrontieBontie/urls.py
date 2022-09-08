from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', ProfileView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('signup/', SignUpView.as_view()),
    path('change-password/', change_password_view),
    path('add-product/', AddProductView.as_view()),
    path('reset-password/', reset_password_view),
]
