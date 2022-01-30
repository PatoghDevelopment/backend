import datetime
from django import utils
from django.db.models import Q
from http.client import ImproperConnectionState, responses
import inspect
from django.db import models
from django.http import response
from rest_framework.decorators import api_view
from django.shortcuts import render

from .models import *
from rest_framework.generics import RetrieveAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from pyotp import otp
from pyotp.totp import TOTP
from rest_framework import permissions , generics, serializers, status
from rest_framework.views import APIView
from .serializers import  EmailSerializer, SignupSerializer
from .serializers import  SignupSerializer, UserProfileSerializer,PatoghSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .models import PendingVerify, User,City,PatoghMembers
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from . import utils
from django.db.models import Count
from rest_framework import viewsets
from django.contrib.auth.models import update_last_login
from django.conf import settings
from django.core.mail import send_mail
import pyotp
import socket
from rest_framework.generics import get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
import pyotp
from .serializers import *

# SignIn Sign out view----------------------
def generateOTP():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, digits=5)
    one_time = totp.now()
    return one_time


class BaseSendOTP(generics.GenericAPIView):
    """
        get just user's email for sending OTP to verify email.
    """

    serializer_class = EmailSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="get otp code",
        responses={
            200: OpenApiResponse(description="EmailTimeError"),
            201: OpenApiResponse(description='sent.'),
            400: OpenApiResponse(description="bad request."),
            401: OpenApiResponse(description="already sign in")
        },
    )
    def post(self, request):
        user_email, obj_user = self.validate_email()
        pending_verify_obj = PendingVerify.objects.filter(receptor=user_email).first()
        otp = generateOTP()
        if pending_verify_obj:
            time_now = timezone.now()
            if time_now > pending_verify_obj.send_time + datetime.timedelta(minutes=2):
                pending_verify_obj.otp = otp
                pending_verify_obj.send_time = time_now
                pending_verify_obj.save()
            else:
                print(user_email)
                return Response(status=status.HTTP_200_OK)
        else:
            instance = PendingVerify(receptor=user_email, otp=otp)
            instance.save()
        print(user_email)
        utils.send_email(otp, user_email)
        return Response(status=status.HTTP_201_CREATED)

    def validate_email(self):
        pass

class SingUpSendOTP(BaseSendOTP):

    def validate_email(self):
        serializer = EmailSerializerSignup(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.data['email']
        obj_user = User.objects.filter(email=user_email).first()
        if not obj_user:
            return user_email, obj_user
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ResetPasswordSendOTP(BaseSendOTP):

    def validate_email(self):
        serializer = EmailSerializerResetPassword(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.data['email']
        obj_user = User.objects.filter(email=user_email).first()
        if obj_user:
            return user_email, obj_user
        return Response(status=status.HTTP_401_UNAUTHORIZED)



# Patogh

class PatoghDetail(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, pk, format=None):
        queryset = Patogh.objects.all().select_related('patogh__patoghinfo').filter(pk=pk)
        serializer = PatoghSerializer()
        
        return Response(serializer.data)

class PatoghDetailLimitedColumn(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, pk, format=None):
        queryset = Patogh.objects.all().select_related('patogh__patoghinfo').filter(pk=pk)
        serializer = PatoghLimitSerializer()
        
        return Response(serializer.data)



# it will send the mail with changed password which is generated randomly


class Signup(generics.CreateAPIView):
    """
         get user's email, password, otp for signup.
    """
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="create a new User",
        responses={
            201: OpenApiResponse(description='Signed UP successfully.'),
            400: OpenApiResponse(description="bad request."),
        },
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.save()
        return Response(data={"email": user_obj.email, "password": user_obj.password}, status=status.HTTP_201_CREATED)


class Signin(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]  
    serializer_class = SigninSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


# for changing the password


class ResetPasswordView(generics.UpdateAPIView):
    serializer_class = RestPasswordSerializer
    model = User
    permission_classes = (permissions.AllowAny,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        email = serializer.validated_data.get('email')
        user = User.objects.filter(email=email).first()
        user.password = serializer.validated_data.get('password1')
        user.save()
        ok_response = {
            'status': 'موفقیت آمیز',
            'code': status.HTTP_200_OK,
            'message': 'پسورد با موفقیت بروز شد',
            'temp': user.password,
            'data': []
        }
        return Response(ok_response)


class UserInfoApiView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class UserProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        return self.request.user


class UserParties(generics.ListAPIView):
    queryset = PartyMembers.objects.all()
    serializer_class = UserPartiesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)