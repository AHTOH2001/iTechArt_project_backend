from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.exceptions import ValidationError

from .models import Profile, Product


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator]
                # https://github.com/encode/django-rest-framework/issues/2996, so unique validator is removed
            }
        }


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

    def update(self, instance, validated_data):
        if 'user' in validated_data:
            user_serializer = self.fields['user']
            user_serializer.update(instance.user, validated_data['user'])
            validated_data.pop('user')

        return super(ProfileSerializer, self).update(instance, validated_data)

    def validate_user(self, user):
        try:
            existing_user = User.objects.get(username=user['username'])
        except User.DoesNotExist:
            return user
        else:
            if existing_user == self.instance.user:
                return user
            else:
                raise ValidationError({'username': ['User with this username already exists']})


class ChangePasswordSerializer(serializers.Serializer):
    password_old = serializers.CharField(max_length=128, min_length=8)
    password_new = serializers.CharField(max_length=128, min_length=8)

    def validate_password_old(self, password_old):
        if not self.instance.check_password(password_old):
            raise ValidationError('Old password is not correct')
        return password_old

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password_new'])
        instance.save()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['category', 'title', 'description', 'price', 'owner']

    # def create(self, validated_data):
    #     product = Product.objects.create(**validated_data, owner=self.)
    #     return product
