from django.contrib.auth import authenticate
from django.db.models import fields
from rest_framework import serializers
from main_app.models import City, User,Gathering
from django.utils.translation import gettext_lazy as _

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id','name']


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("نام کاربری"),
        write_only=True        
    )

    email = serializers.EmailField(
        label=_("ایمیل"),
        write_only = True,
    )

    password1 = serializers.CharField(
        label= _("رمز عبور"),
        min_length = 6,
        write_only = True,
        help_text =_("رمز عبور باید حداقل 6 کاراکتر باشد")
    )

    password2 = serializers.CharField(
        label= _("تکرار رمز عبور"),
        min_length = 6,
        write_only = True,
        help_text =_("رمز عبور باید حداقل 6 کاراکتر باشد")
    )

    fullname = serializers.CharField(
        label = _("نام"),
        write_only = True
    )

    token = serializers.CharField(
        label = _("توکن"),
        read_only = True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if email and username and password1 and password2 and (password1 == password2):
            user = authenticate(request=self.context.get('request'),
                                username=username, password = password1)
            if user:
                msg = _("کاربر با این مشخصات وجود دارد")
                raise serializers.ValidationError(msg, code= 'conflict')
        else:
            msg = _("اطلاعات کابر باید به درستی و کامل وارد شود")
            raise serializers.ValidationError(msg, code = 'authorization')
      
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_("کاربر با این ایمیل وجود دارد"))

        return attrs

    def create(self , validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password1']
        fullname = validated_data['fullname']
        otp = validated_data['otp']

        user = User.objects.create_user(username,email,password,fullname,otp)
        return user

class SigninSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("نام کاربری"),
        write_only=True        
    )

    password = serializers.CharField(
        label= _("رمز عبور"),
        min_length = 6,
        write_only = True,
        help_text =_("رمز عبور باید حداقل 6 کاراکتر باشد")
    )

    token = serializers.CharField(
        label = _("توکن"),
        read_only = True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password :
            user1 = authenticate(request=self.context.get('request'),
                                username=username, password = password)
            
            if User.objects.filter(email=username).exists():
                user2 = User.objects.get(email = username)
            
            if not (user1 or user2):
                msg = _("کاربر با این مشخصات وجود ندارد")
                raise serializers.ValidationError(msg, code= 'authorization')
        else:
            msg = _("اطلاعات کابر باید به درستی و کامل وارد شود")
            raise serializers.ValidationError(msg, code = 'authorization')

        if user1:
            attrs['user'] = user1
        else:
            attrs['user'] = user2

        return attrs

class UserSerializer(serializers.ModelSerializer):
    is_confirmed = serializers.SerializerMethodField()
    city = CitySerializer()

    class Meta:
        model = User
        fields = ['fullname','phone','birthdate','city','gender','profile_image_url','bio','is_confirmed']
        read_only_fields = ['is_confirmed']

    def get_is_confirmed(slef , obj):
        return obj.is_confirmed

    def update(self, instance, validated_data):
        city = validated_data.pop('city')
        instance.city = city.id
        instance.save()
        return instance

class VerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['otp']

class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ('email',)


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    fields = ['username','fullname','email','phone','birthdate','city','gender','profile_image_url','bio']
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class GhatheringListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gathering
        fields = '__all__'
        depth = 1
