import datetime
from django import utils
from django.db.models import Q
from http.client import ImproperConnectionState, responses
import inspect
from django.db import models
from django.http import response
from rest_framework.decorators import api_view
from django.shortcuts import render

from .models import Patogh
from rest_framework.generics import RetrieveAPIView, ListAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny
from pyotp import otp
from pyotp.totp import TOTP
from rest_framework import permissions , generics, serializers, status
from rest_framework.views import APIView
from main_app.serializers import  EmailSerializer, SignupSerializer
from .serializers import  SignupSerializer, UserProfileSerializer,PatoghSerializer
from .serializers import ChangePasswordSerializer
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from main_app.models import PendingVerify, User,City,PatoghMembers
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

# SignIn Sign out view----------------------
def generateOTP():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, digits=5)
    one_time = totp.now()
    return one_time


class SendOTP(generics.GenericAPIView):
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
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.data['email']
        obj_user = User.objects.filter(email=user_email).first()
        pending_verify_obj = PendingVerify.objects.filter(receptor=user_email).first()
        otp = generateOTP()
        if not obj_user:
            if pending_verify_obj:
                time_now = timezone.now()
                if time_now > (pending_verify_obj).send_time + datetime.timedelta(minutes=2):
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
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


# Patogh
class PatoghDetail(RetrieveAPIView):
    queryset = Patogh.objects.all()
    serializer_class = PatoghSerializer
    permission_classes = (AllowAny,)

class PatoghDetailWithSearch(ListAPIView):
    queryset = Patogh.objects.all()
    serializer_class = PatoghSerializer
    permission_classes = (AllowAny,)
    # filterset_fields = ['id']
    # search_fields =  ['patoghInfo__name'] i will fiex this




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
        serializer = self.serializer_class(data=request.data)
        # Generating Random Password of specific Type or use according to your need
        str_1 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z']
        str_2 = ['!', '@', '#', '$', '%', '&', '*', '/', '-', '+']
        str_3 = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

        str = random.choice(str_1)
        for s in range(4):
            str += random.choice(str_1).lower()
        str += random.choice(str_2)
        for x in range(2):
            str += random.choice(str_3)

        password = handler.hash(str)

        if serializer.is_valid():
            email = request.data['email']
            User.objects.filter(email=email).update(password=password)

            subject = 'Forgot Password Request'
            message = 'Your request for Forgot Password has been received, your new password is ' + str
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]

            send_mail(
                subject,
                message,
                email_from,
                recipient_list,
                fail_silently=False,
            )
            return Response({'msg': 'done'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'Not a valid request'}, status=status.HTTP_400_BAD_REQUEST)

# for changing the password

class ChangePasswordView(generics.UpdateAPIView):

        serializer_class = ChangePasswordSerializer
        model = User
        permission_classes = (permissions.IsAuthenticated,)

        http_method_names = ['put']
        
        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"پسورد قدیمی": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'موفقیت آمیز',
                    'code': status.HTTP_200_OK,
                    'message': 'پسورد با موفقیت بروز شد',
                    'data': []
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.AllowAny,)

    # @extend_schema(
    #     summary="update profile",
    #     responses={
    #         201: OpenApiResponse(response=SignupSerializer,
    #                              description=''),
    #         400: OpenApiResponse(
    #             description=""),
    #     },
    # )
    # def put(self, request, *args, **kwargs):        # update profile
    #     return super(UserProfileView, self).put(request)
    #
    # @extend_schema(
    #     summary="get user info",
    #     responses={
    #         201: OpenApiResponse(response=SignupSerializer,
    #                              description=''),
    #         400: OpenApiResponse(
    #             description=""),
    #     },
    # )
    # def get(self, request, *args, **kwargs):        # get user info
    #     return super(UserProfileView, self).get(request)

