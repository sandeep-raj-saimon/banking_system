from django.db import models
from userservice.models import *
# Create your models here.


class Wallet(models.Model):
    id = models.AutoField(primary_key=True, default=None)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    account_number = models.CharField()
    opening_balance = models.DecimalField(decimal_places=5, max_digits=20)
    closing_balance = models.DecimalField(decimal_places=5, max_digits=20)

    objects = models.Manager()

    def __str__(self):
        return self.closing_balance


class Transaction(models.Model):
    id = models.AutoField(primary_key=True, null=False)
    payee = models.ForeignKey(
        UserProfile, on_delete=models.RESTRICT, related_name='payee')
    payer = models.ForeignKey(
        UserProfile, on_delete=models.RESTRICT, related_name='payer')
    payee_wallet = models.ForeignKey(
        Wallet, on_delete=models.RESTRICT, related_name='payee_account')
    payer_wallet = models.ForeignKey(
        Wallet, on_delete=models.RESTRICT, related_name='payer_account')
    amount = models.DecimalField(decimal_places=5, max_digits=20)
    created_at = models.DateField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return self.amount
