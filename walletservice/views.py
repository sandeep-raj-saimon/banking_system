from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *
from django.forms.models import model_to_dict
from random import randrange

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
        return Response({"message": "New wallet has been created"})

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

        transaction_id = request.GET.get('id')
        if transaction_id is None:
            return CustomResponse(None, "error", status.HTTP_401_UNAUTHORIZED).response()

    def post(self, request):
        if request.user.is_authenticated == False:
            return CustomResponse(None, "error",  status.HTTP_401_UNAUTHORIZED).response()
