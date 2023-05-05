from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.


class Wallet(APIView):
    def get(self, request):
        return Response({"message": "All wallets"})

    def post(self, request):
        return Response({"message": "New wallet has been created"})
