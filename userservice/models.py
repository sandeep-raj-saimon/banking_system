from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser, UserManager, PermissionsMixin
# Create your models here.


class UserProfile(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, default=None)
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(null=True)
    is_superuser = models.BooleanField(null=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    objects = UserManager()
