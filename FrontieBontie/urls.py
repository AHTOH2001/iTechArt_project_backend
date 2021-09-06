from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', ProfileView.as_view()),
    path('logout/', LogOutView.as_view()),
]
