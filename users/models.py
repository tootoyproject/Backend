from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser


# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=50,)
    
    def __str__(self):
        return self.username