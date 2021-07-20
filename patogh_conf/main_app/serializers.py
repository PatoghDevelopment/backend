from django.contrib.auth import authenticate
from rest_framework import serializers
from main_app.models import City, User, Gathering,GatheringHaveMember
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import get_object_or_404

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

    city = serializers.PrimaryKeyRelatedField(source='supporters', queryset=City.objects.all(),
                                                        many=True, required=False)

    class Meta:
        model = User
        fields = ['fullname','phone','birthdate','city','gender','profile_image_url','bio']
   

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
        fields = ['username','fullname','email','phone','birthdate','city','gender','profile_image_url','bio']
    


class GhatheringListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gathering
        fields = ['id','creator_id','patogh_id','name','status','start_time','end_time','description','gender_filter','members_count','min_age','max_age','tags_id']
        depth = 1

class TopUsersSerializer(serializers.Serializer):
    class Meta:
        model = GatheringHaveMember
        fields = ['username']
    
class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id','name']
        read_only_fields = ['id']