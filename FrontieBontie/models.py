from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Category(models.Model):
    title = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'categories'


class Product(models.Model):
    category = models.ForeignKey(to=Category, on_delete=models.PROTECT)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2, validators=[MinValueValidator(0.009)])
    owner = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
