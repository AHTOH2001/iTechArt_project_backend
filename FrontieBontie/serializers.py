from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Profile
        fields = ['user']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data['user'])
        validated_data.pop('user')
        profile = Profile.objects.create(**validated_data, user=user)
        return profile
