from django.contrib.auth import authenticate
from rest_framework import serializers
from main_app.models import User, validate_image_size
from django.utils.translation import gettext_lazy as _

class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(
        label=_("نام کاربری"),
        write_only=True        
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
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')

        if username and password1 and password2 and (password1 == password2):
            user = authenticate(request=self.context.get('request'),
                                username=username, password = password1)
            if user:
                msg = _("کاربر با این مشخصات وجود دارد")
                raise serializers.ValidationError(msg, code= 'conflict')
        else:
            msg = _("اطلاعات کابر باید به درستی و کامل وارد شود")
            raise serializers.ValidationError(msg, code = 'authorization')

        return attrs

    def create(self , validated_data):
        username = validated_data['username']
        password = validated_data['password1']
        
        user = User.objects.create_user(username,password)
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
            user = authenticate(request=self.context.get('request'),
                                username=username, password = password)
            if not user:
                msg = _("کاربر با این مشخصات وجود ندارد")
                raise serializers.ValidationError(msg, code= 'authorization')
        else:
            msg = _("اطلاعات کابر باید به درستی و کامل وارد شود")
            raise serializers.ValidationError(msg, code = 'authorization')

        attrs['user'] = user

        return attrs