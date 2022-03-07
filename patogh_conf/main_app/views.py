from django import utils
from django.contrib.auth.hashers import make_password
from rest_framework.generics import get_object_or_404
from rest_framework import permissions, generics, status
from rest_framework.authtoken.models import Token
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from . import utils
import pyotp
from .serializers import *


def generateOTP():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret, digits=5)
    one_time = totp.now()
    return one_time


class BaseSendOTP(generics.GenericAPIView):
    def validate_email(self):
        pass

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


class SingUpSendOTP(BaseSendOTP):
    def validate_email(self):
        serializer = EmailSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.data['email']
        obj_user = User.objects.filter(email=user_email).first()
        if not obj_user:
            return user_email, obj_user
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ForgotPasswordSendOTP(BaseSendOTP):
    def validate_email(self):
        serializer = EmailSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.data['email']
        obj_user = User.objects.filter(email=user_email).first()
        if obj_user:
            return user_email, obj_user
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class Signup(generics.CreateAPIView):
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
    serializer_class = SigninSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class ForgotPasswordView(generics.UpdateAPIView):
    serializer_class = ForgotPasswordSerializer
    model = User
    permission_classes = [permissions.AllowAny]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        email = serializer.validated_data.get('email')
        user = User.objects.filter(email=email).first()
        user.password = make_password(serializer.validated_data.get('password1'))
        user.save()
        ok_response = {
            'status': 'موفقیت آمیز',
            'code': status.HTTP_200_OK,
            'message': 'پسورد با موفقیت بروز شد',
            'data': []
        }
        return Response(ok_response)


class Profile(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserProfile(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])


class DeleteAccount(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        user.delete()
        return Response(status=status.HTTP_200_OK)


class ChangePassword(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if hasattr(user, 'auth_token'):
            user.auth_token.delete()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)


class Support(generics.CreateAPIView):
    serializer_class = Support

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


# Patogh

"""class PatoghDetail(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk, format=None):
        queryset = Patogh.objects.all().select_related('patogh__patoghinfo').filter(pk=pk)
        serializer = PatoghSerializer()

        return Response(serializer.data)"""

"""class PatoghDetailLimitedColumn(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, pk, format=None):
        queryset = Patogh.objects.all().select_related('patogh__patoghinfo').filter(pk=pk)
        serializer = PatoghLimitSerializer()

        return Response(serializer.data)"""

"""class PatoghCreateAndUpdateAndDelete(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, format=None):
        serializer = PatoghAndOtherModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        patoghInfo = self.get_object(pk)
        patoghInfo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        patoghinfo = self.get_object(pk)
        serializer = PatoghAndOtherModelSerializer(patoghinfo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)"""


class UserParties(generics.ListAPIView):
    queryset = PartyMembers.objects.all()
    serializer_class = UserPartiesSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class FriendRequestListCreate(generics.ListCreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(receiver=self.request.user)

    def perform_create(self, serializer):
        if FriendRequest.objects.filter(sender=self.request.user,
                                        receiver=get_object_or_404(User, username=self.kwargs['username'])).exists():
            return Response('شما قبلا به این کاربر درخواست داده اید', status=400)
        if self.request.user.friends.filter(username=self.kwargs['username']).exists():
            raise Response('این کاربر از دوستان شماست', status=400)
        serializer.save(sender=self.request.user,
                        receiver=get_object_or_404(User, username=self.kwargs['username']))


class AcceptFriendRequest(generics.CreateAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs['username'])
        req = get_object_or_404(FriendRequest, sender=user, receiver=self.request.user)
        self.request.user.friends.add(user)
        user.friends.add(self.request.user)
        req.delete()
        return Response('Accepted', status=201)


class RemoveFriendRequest(generics.DestroyAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs['username'])
        req = get_object_or_404(FriendRequest, sender=user, receiver=self.request.user)
        req.delete()
        return Response('Deleted', status=200)


class FriendList(generics.ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.friends.all()


class RemoveFriend(generics.DestroyAPIView):
    serializer_class = FriendSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.kwargs['username'])
        if not user.friends.filter(username=self.request.user.username).exists():
            return Response('این کاربر از دوستان شما نیست', status=400)
        user.friends.remove(self.request.user)
        self.request.user.friends.remove(user)
        return Response('Deleted', status=210)


class SearchUser(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(username=self.kwargs['username'])


class CompanyCreate(generics.CreateAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        obj = serializer.save(creator=self.request.user)
        obj.members.add(self.request.user)


class CompanyList(generics.ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.company_set.all()


class AddCompanyMember(generics.CreateAPIView):
    serializer_class = FriendSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.company_set.all()

    def post(self, request, *args, **kwargs):
        company = get_object_or_404(Company, pk=self.kwargs['pk'])
        user = get_object_or_404(User, username=self.kwargs['username'])
        if company.creator.username != self.request.user.username:
            return Response('فقط سازنده گروه حق اضافه کردن عضو جدید را دارد', status=400)
        if company.members.filter(username=user.username).exists():
            return Response('کاربر مورد نظر از اعضای گروه میباشد', status=400)
        company.members.add(user)
        return Response('اضافه شد', status=201)


class LeaveCompany(generics.CreateAPIView):
    serializer_class = LeaveCompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.company_set.all()

    def post(self, request, *args, **kwargs):
        company = get_object_or_404(Company, pk=self.kwargs['pk'])
        if company.creator == self.request.user:
            company.delete()
            return Response('با خروج شما اکیپ حذف شد', status=200)
        if company.members.filter(username=self.request.user.username).exists():
            company.members.remove(self.request.user)
            return Response('Left', status=201)
        else:
            return Response('شما عضو این گروه نیستید', status=400)


class RemoveMember(generics.DestroyAPIView):
    serializer_class = FriendSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.company_set.all()

    def delete(self, request, *args, **kwargs):
        company = get_object_or_404(Company, pk=self.kwargs['pk'])
        user = get_object_or_404(User, username=self.kwargs['username'])
        if company.creator != self.request.user:
            return Response('فقط سازنده اکیپ به این قابلیت دسترسی دارد', status=200)
        if not company.members.filter(username=user.username).exists():
            return Response('کاربر مورد نظر از اعضای گروه نمیباشد', status=400)
        company.members.remove(user)
        return Response('Deleted', status=200)


class CompanyMembers(generics.ListAPIView):
    serializer_class = FriendSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return get_object_or_404(Company, pk=self.kwargs['pk']).members.all()


class CompanyRUD(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanyRUDSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Company.objects.all()

    def perform_authentication(self, request):
        company = get_object_or_404(Company, pk=self.kwargs['pk'])
        if company.creator != self.request.user:
            raise ValidationError('فقط سازنده اکیپ به این قابلیت دسترسی دارد')


class CompanySearch(generics.ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Company.objects.filter(name=self.kwargs['name'], members__in=[self.request.user])
