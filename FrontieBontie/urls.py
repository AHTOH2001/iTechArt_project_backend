from django.urls import path
from .views import *

urlpatterns = [
    path('page/', SecurePage.as_view())
]
