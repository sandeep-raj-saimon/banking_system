from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.forms.models import model_to_dict
from random import randrange
from django.db import transaction

# Create your views here.


class CustomResponse():
    def __init__(self, data, message, status_code):
        self.data = data
        self.message = message
        self.status_code = status_code

    def response(self):
        return Response({
            "message": self.message,
            "data": self.data,
            "status_code": self.status_code,
        })


class Wallets(APIView):
    def get(self, request):
        if request.user.is_authenticated == False:
            return CustomResponse(None, "error",  status.HTTP_401_UNAUTHORIZED).response()

        account_numer = request.GET.get('acc_num')
        current_user = request.user

        if account_numer is None:
            return CustomResponse(None, "error", status.HTTP_401_UNAUTHORIZED).response()

        try:
            current_wallet = current_user.wallets.filter(
                account_number=account_numer).first()
            return CustomResponse(model_to_dict(current_wallet), "success", status.HTTP_200_OK).response()
        except Exception as e:
            print(e)
            return CustomResponse(None, "Wallet does not exists", status.HTTP_404_NOT_FOUND).response()

    def post(self, request):
        body = request.data
        opening_balance = body.get('opening_balance')
        closing_balance = body.get('closing_balance')
        account_number = self.get_account_number()

        if request.user.is_authenticated == False:
            return CustomResponse(None, "error",  status.HTTP_401_UNAUTHORIZED).response()

        Wallet.objects.create(
            user=request.user,
            opening_balance=opening_balance,
            closing_balance=closing_balance,
            account_number=account_number
        )
        return CustomResponse(None, "A new account has been created",  status.HTTP_201_CREATED).response()

    def get_account_number(self):
        account_number = ""
        for i in range(16):
            account_number += str(randrange(0, 9))

        try:
            Wallet.objects.get(account_number=account_number)
            self.get_account_number()
        except:
            return account_number


class Transactions(APIView):
    def get(self, request):
        if request.user.is_authenticated == False:
            return CustomResponse(None, "error",  status.HTTP_401_UNAUTHORIZED).response()

        transaction_id = request.GET.get('transaction_id')
        transaction_type = request.GET.get('transaction_type')
        account_number = request.GET.get('account_number')
        current_user = request.user

        if transaction_id is None or account_number is None:
            return CustomResponse(None, "Transaction Id Or Account Number is mandatory", status.HTTP_401_UNAUTHORIZED).response()

        try:
            current_wallet = current_user.wallets.filter(
                account_number=account_number).first()
            if current_wallet is None:
                return CustomResponse(None, "Wallet not found", status.HTTP_401_UNAUTHORIZED).response()

            transaction = None
            if transaction_type == "send":
                transaction = current_wallet.payer_account_transactions.filter(
                    payer_wallet=current_wallet, id=transaction_id).first()
            elif transaction_type == "receive":
                transaction = current_wallet.payer_account_transactions.filter(
                    payer_wallet=current_wallet, id=transaction_id).first()
            else:
                return CustomResponse(None, "Invalid transaction type", status.HTTP_400_BAD_REQUEST).response()

            if transaction is None:
                return CustomResponse(None, "No transaction found", status.HTTP_400_BAD_REQUEST).response()

            return CustomResponse(model_to_dict(transaction), "success", status.HTTP_200_OK).response()
        except:
            return CustomResponse(model_to_dict(transaction), "Something went wrong", status.HTTP_200_OK).response()

    def post(self, request):
        if request.user.is_authenticated == False:
            return CustomResponse(None, "error",  status.HTTP_401_UNAUTHORIZED).response()

        body = request.data
        user_id = body.get("user_id")

        if user_id is None:
            return CustomResponse(None, "User Id is mandatory",  status.HTTP_400_BAD_REQUEST).response()

        payer = request.user
        payee = UserProfile.objects.get(id=user_id)

        payee_account_number = body.get("payee_account_number")
        payer_account_number = body.get("payer_account_number")
        amount = body.get("amount")

        payee_account = payee.wallets.filter(
            account_number=payee_account_number).first()
        payer_account = payer.wallets.filter(
            account_number=payer_account_number).first()

        print(payee_account, "sdas", payer_account)
        if payee_account is None or payer_account is None:
            return CustomResponse(None, "One of the account is wrong",  status.HTTP_400_BAD_REQUEST).response()
        if payer_account.closing_balance < amount:
            return CustomResponse(None, "User does not have appropriate balance",  status.HTTP_400_BAD_REQUEST).response()

        try:
            with transaction.atomic():
                Transaction.objects.create(
                    payer=payer,
                    payee=payee,
                    payer_wallet=payer_account,
                    payee_wallet=payee_account,
                    amount=amount)

                payee_account.closing_balance += amount
                payer_account.closing_balance -= amount

                payee_account.save()
                payer_account.save()
        except Exception as e:
            print(e)
            return CustomResponse(None, "Transaction could not be completed",  status.HTTP_400_BAD_REQUEST).response()

        return CustomResponse(None, "Transaction has been completed",  status.HTTP_201_CREATED).response()
