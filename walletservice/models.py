from django.db import models
from userservice.models import *
# Create your models here.


class Wallet(models.Model):
    id = models.AutoField(primary_key=True, default=None)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    opening_balance = models.DecimalField(decimal_places=5, max_digits=20)
    closing_balance = models.DecimalField(decimal_places=5, max_digits=20)

    wallets = models.Manager()

    def __str__(self):
        return self.closing_balance

# class Transactions(models.Model):
#     user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     amount =
