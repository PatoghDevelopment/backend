from http.client import responses
from django.http import response
from django.shortcuts import render
from rest_framework import permissions , generics, serializers, status
from main_app.serializers import SignupSerializer, SigninSerializer, UserSerializer
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from main_app.models import User

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