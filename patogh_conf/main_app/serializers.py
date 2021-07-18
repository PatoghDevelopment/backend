from django.contrib.auth import authenticate
from django.db.models import fields
from rest_framework import serializers
from main_app.models import IDENTIFIED, User
from django.utils.translation import gettext_lazy as _
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
        
        user = User.objects.create_user(username,email,password)
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
    is_identified = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username','fullname','email','phone','birthdate','city','gender','profile_image_url','bio','identity_state']
    
    def get_is_identified(slef , obj):
        return obj.identity_state == IDENTIFIED