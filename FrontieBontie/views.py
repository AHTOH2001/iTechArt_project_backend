from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class SecurePage(RetrieveAPIView):
    """This page is created only for test JWT auth"""
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response({'Yak': 'slishna?'})
