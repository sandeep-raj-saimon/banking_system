from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
from rest_framework import status

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


class User(APIView):
    def get(self, request):
        if request.user.is_authenticated == False:
            return CustomResponse(None, "error",  status.HTTP_401_UNAUTHORIZED).response()

        user_id = request.GET.get('id')
        if user_id == None:
            return CustomResponse(None, "error", status.HTTP_401_UNAUTHORIZED).response()
        try:
            user = UserProfile.objects.get(id=user_id)
            return CustomResponse(model_to_dict(user), "success", status.HTTP_200_OK).response()
        except:
            return CustomResponse(None, "User does not exists", status.HTTP_404_NOT_FOUND).response()

    def post(self, request):
        body = request.data
        username = body.get('username')
        password = body.get('password')
        email = body.get('email')

        if username is None or password is None:
            return CustomResponse(None, "Credentials are required", status.HTTP_400_BAD_REQUEST).response()

        try:
            current_user = UserProfile.objects.get(username=username)
            if check_password(password, current_user.password) is True:
                access_token = RefreshToken.for_user(current_user).access_token
                return CustomResponse(str(access_token), "User already exists", status.HTTP_200_OK).response()
            else:
                return CustomResponse(None, "Wrong credentials", status.HTTP_400_BAD_REQUEST).response()
        except:

            new_user = UserProfile.objects.create_user(
                username, email)
            new_user.set_password(password)
            new_user.save()

            access_token = RefreshToken.for_user(new_user).access_token
            return CustomResponse(str(access_token), "New User has been created", status.HTTP_201_CREATED).response()

    def update(self, request):
        if request.user.is_authenticated == False:
            return CustomResponse(None, "error",  status.HTTP_401_UNAUTHORIZED).response()

        user_id = request.GET.get('id')
        body = request.data

    def delete(self, request):
        if request.user.is_authenticated == False:
            return CustomResponse(None, "error",  status.HTTP_401_UNAUTHORIZED).response()

        user_id = request.GET.get('id')
        UserProfile.objects.get(id=user_id).delete()
        return CustomResponse(None, "success", status.HTTP_200_OK)


class Logout(APIView):
    def get(self, request):
        if request.user.is_authenticated == False:
            return CustomResponse(None, "error",  status.HTTP_401_UNAUTHORIZED).response()
        request.user.auth_token.delete()
        return CustomResponse(None, "success", status.HTTP_200_OK)
