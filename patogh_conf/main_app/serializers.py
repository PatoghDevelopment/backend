from django.contrib.auth import authenticate
from rest_framework import serializers
from main_app.models import City, PendingVerify, User
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from django.utils import timezone
import datetime


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


from .models import Patogh

class SignupSerializer(serializers.Serializer):

    email = serializers.EmailField(
        label=_("ایمیل"),
        write_only=True
        )

    otp = serializers.CharField(
        label=_("توکن"),
        write_only=True
    )
    
    password1 = serializers.CharField(
        label=_("1رمز عبور"),
        min_length=6,
        max_length=30,
        write_only=True,
        help_text=_("رمز عبور باید حداقل 6 کاراکتر باشد")
    )
    
    password2 = serializers.CharField(
        label=_("2رمز عبور"),
        min_length=6,
        max_length=30,
        write_only=True,
        help_text=_("رمز عبور باید حداقل 6 کاراکتر باشد")
    )


    def validate(self, attrs):
        email = attrs.get('email')
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if email and password1 and password2:
            if User.objects.filter(email=email).exists():
                msg = _("کاربر با این مشخصات وجود دارد")
                raise serializers.ValidationError(msg, code='conflict')
            if password1 != password2:
                msg = _("لطفا هردو گذرواژه را یکسان وارد نمایید")
                raise serializers.ValidationError(msg, code='conflict')
            # user = authenticate(request=self.context.get('request'), password=password)
            # if user:
            else:
                otp = attrs.get('otp')
                pending_verify_obj = PendingVerify.objects.filter(receptor=email).first()
                time_now = timezone.now()
                if time_now < pending_verify_obj.send_time + datetime.timedelta(minutes=2):
                    if int(otp) == pending_verify_obj.otp:
                        return attrs
                    else:
                        raise serializers.ValidationError(_("کد تایید وارد شده اشتباه است."))
                else:
                    raise serializers.ValidationError(_("کد تایید منقضی شده است."))

        else:
            msg = _("اطلاعات کابر باید به درستی و کامل وارد شود")
            raise serializers.ValidationError(msg, code='authorization')

    def create(self, validated_data):
        email = validated_data['email']
        password1 = validated_data['password1']
        # otp = validated_data['otp']
        user = User.objects.create_user(email, password1)
        PendingVerify.objects.filter(receptor=email).delete()
        return user


class SigninSerializer(serializers.Serializer):
    email = serializers.EmailField(
        label="ایمیل",
        write_only=True
    )
    password = serializers.CharField(
        label="رمز عبور",
        min_length=6,
        write_only=True,
        help_text="رمز عبور باید حداقل ۶ رقمی باشد"
    )
    token = serializers.CharField(
        label="توکن",
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # user = authenticate(request=self.context.get('request'),
            #                     email=email, password=password)
            user = User.objects.filter(email = email, password = password)
            if user.exists():
                user = user.first()

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.'+user[0])
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class UserSerializer(serializers.ModelSerializer):

    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), many=True, required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'email', 'birthdate', 'city', 'avatar', 'mobile_number', 'bio']
   

class VerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['otp']

class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email']


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'email', 'birthdate', 'city', 'avatar', 'mobile_number', 'bio']
    

class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id','name']
        read_only_fields = ['id']

    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'gender', 'email', 'birthdate', 'city', 'avatar', 'mobile_number', 'bio', 'score']
        read_only_fields = ['email']


class PatoghSerializer(serializers.ModelSerializer):
    
    patogh_id = serializers.SerializerMethodField("get_patogh_id")

    def get_patogh_id(self, obj):
        return {
            "id" : obj.patogh_id.id,
            "creator" : obj.patogh_id.creator,
            "name" : obj.patogh_id.name,
        }
    
    class Meta:
        model = Patogh
        fields = "__all__"

