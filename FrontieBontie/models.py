from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Product(models.Model):
    category = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.009)])
    owner = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
