from http.client import responses
from django.http import response
from django.shortcuts import render
from rest_framework import permissions, generics, serializers, status, viewsets
from rest_framework.decorators import api_view

from .serializers import SignupSerializer, SigninSerializer, UserSerializer, AddDorehamiSerializer
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .models import User, City

from .models import Gathering
from .serializers import UserProfileSerializer, GhatheringListSerializer


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
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

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

class UserInfoApiView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user

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