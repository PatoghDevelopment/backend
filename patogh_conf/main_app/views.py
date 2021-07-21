import datetime
from http.client import ImproperConnectionState, responses
import inspect
from django.db import models
from django.http import response
from rest_framework.decorators import api_view
from django.shortcuts import render
from pyotp import otp
from pyotp.totp import TOTP
from rest_framework import permissions , generics, serializers, status
from rest_framework.views import APIView
from main_app.serializers import AddDorehamiSerializer, CityListSerializer, SignupSerializer,SigninSerializer, TopUsersSerializer, UserProfileSerializer,VerifyOTPSerializer
from main_app.serializers import UserSerializer,ForgotPasswordSerializer
from main_app.serializers import ChangePasswordSerializer
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from main_app.models import GatheringHaveMember, User,City,Gathering
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import random
from django.db.models import Count
from rest_framework import viewsets
from passlib.hash import django_pbkdf2_sha256 as handler
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.conf import settings
from django.core.mail import send_mail
import jwt
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
import pyotp
import socket

socket.getaddrinfo('127.0.0.1', 8080)

otp_code = 0
global totp

def generateOTP():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, interval=3000)
    one_time = totp.now()

    return one_time

# verifying OTP


def verifyOTP(one_time, user):
    if user.otp == one_time:
        return True
    else:
        return False



class SignupApiView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary = "create a new User",
        responses={
            201: OpenApiResponse(response=SignupSerializer,
                                    description='Created.'),
            400: OpenApiResponse(description="bad request, user exist or you have to make sure you fill the necessary fields correctly."),
        },
    )
    

    def post(self, request):
        email = request.data['email']
        name = request.data['username']

        data = User.objects.filter(email=email)

        if data.exists():
            return Response({'msg': 'کاربر با این مشخصات وجود دارد'}, status=status.HTTP_409_CONFLICT)
        else:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                otp_code = generateOTP()
                serializer.save(otp=otp_code)
                message = f'Welcome {name} Your OTP is : ' + \
                    otp_code
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [email]
                message = message
                subject = "OTP" 
                send_mail(
                    subject,
                    message,
                    email_from,
                    recipient_list,
                    fail_silently=False,
                )

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({"Error": "Sign Up Failed"}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        user = User.objects.get(username=serializer.validated_data['username'])
        token , created = Token.objects.get_or_create(user = user)
        data = {
            'token' : token.key
        }

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save(otp=otp_code)

class SigninApiView(generics.GenericAPIView):
    permissions = [permissions.AllowAny]
    serializer_class = SigninSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
 
        user = serializer.validated_data['user']
        token , created = Token.objects.get_or_create(user = user)
        data = {
            'token' : token.key
        }

        return Response(data)

class CityListCreateApi(generics.ListCreateAPIView):
    serializer_class = CityListSerializer
    permission_classes = (permissions.AllowAny,)

    queryset = City.objects.all()

    def perform_create(self, serializer):
        serializer.save()
        

class UserInfoApiView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_object(self):
        return self.request.user

class VerifyOTPView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = VerifyOTPSerializer

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        one_time = serializer.validated_data['otp']
        user = self.request.user
        username = user.username
        one = verifyOTP(one_time,user)
        if one:
            User.objects.filter(username=username).update(
                is_confirmed=True, otp=one_time)
            return Response({'msg': 'OTP verfication successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'msg': 'OTP verfication Failed'}, status=status.HTTP_400_BAD_REQUEST)

# it will send the mail with changed password which is generated randomly


class ForgotPasswordView(APIView):
    serializer_class = ForgotPasswordSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
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


class TopUsersApiView(generics.ListAPIView):
    serializer_class = TopUsersSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        result = GatheringHaveMember.objects.all().values('username_id').annotate(total=Count('username_id')).order_by('-total')[0:3]
        return result


@api_view(['POST'])
def AddDorehami(request):
    data = {
        'id': request.data['id'],
        'creator_id': request.data['creator_id'],
        'patogh_id': request.data['patogh_id'],
        'name': request.data['name'],
        'status': request.data['status'],
        'start_time': request.data['start_time'],
        'end_time': request.data['end_time'],
        'description': request.data['description'],
        'gender_filter ': request.data['gender_filter '],
        'members_count': request.data['members_count'],
        'min_age': request.data['min_age'],
        'max_age': request.data['max_age'],
        'tags_id': request.data['tags_id'],
    }
    ser = AddDorehamiSerializer(data=data)
    if ser.is_valid():
        ser.save()
        return Response(ser.data, status.HTTP_201_CREATED)
    else:
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def SearchDorehami(request):
    dorehamiha = Gathering.objects.all()
    try:
        name = request.query_params['name']
        if name:
            dorehamiha = Gathering.objects.filter(name=name)
    except:
        pass
    try:
        Mcity = City.objects.get(name=request.query_params['name'])
        city_id = Mcity.id
        if Mcity:
            dorehamiha = Gathering.objects.filter(city=city_id)
    except:
        pass
    try:
        gender_filter = request.query_params['gender_filter']
        if gender_filter:
            dorehamiha = Gathering.objects.filter(gender_filter=gender_filter)
    except:
        pass
    try:
        members_count = request.query_params['members_count']
        if members_count:
            dorehamiha = Gathering.objects.filter(members_count=members_count)
    except:
        pass
    try:
        start_time = request.query_params['start_time']
        if start_time:
            dorehamiha = Gathering.objects.filter(start_time=start_time)
    except:
        pass
    if dorehamiha:
        ser = AddDorehamiSerializer(dorehamiha,many=True)
        return  Response(ser.data,status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def UserProfile(request):
    SpecificUser = User.objects.all()
    try:
        id = request.query_params['id']
        if id:
            SpecificUser = User.objects.filter(id=id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        ser = UserProfileSerializer(SpecificUser)
        return Response(ser.data,status=status.HTTP_200_OK)
    except:
        pass