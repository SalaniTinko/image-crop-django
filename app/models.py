

from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
from django.utils import timezone


class CropModel(models.Model):
    image = models.ImageField()
    time = models.DateTimeField(auto_now_add=True)
    bucket_name = models.CharField(max_length=30)
    bucket_url = models.URLField()
class CustomOrder(models.Model):
    amount = models.FloatField(default=True,null=True)
    created_at = models.DateTimeField(default=timezone.now())