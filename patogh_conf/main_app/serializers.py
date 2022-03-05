from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from django.utils import timezone
import datetime


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmailSerializerResetPassword(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')

        if email:
            if not User.objects.filter(email=email).exists():
                msg = _("کاربر با این مشخصات وجود ندارد")
                raise serializers.ValidationError(msg, code='authorization')
        #     else:
        #         msg = _("کاربر با این مشخصات وجود ندارد")
        #         raise serializers.ValidationError(msg, code= 'authorization')
        # else:
        #     msg = _("اطلاعات کابر باید به درستی و کامل وارد شود")
        #     raise serializers.ValidationError(msg, code = 'authorization')

        # if user1:
        #     attrs['user'] = user1
        return attrs


class EmailSerializerSignup(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')

        if email:
            if User.objects.filter(email=email).exists():
                msg = _("کاربر با این مشخصات وجود دارد")
                raise serializers.ValidationError(msg, code='authorization')
        #     else:
        #         msg = _("کاربر با این مشخصات وجود ندارد")
        #         raise serializers.ValidationError(msg, code= 'authorization')
        # else:
        #     msg = _("اطلاعات کابر باید به درستی و کامل وارد شود")
        #     raise serializers.ValidationError(msg, code = 'authorization')

        # if user1:
        #     attrs['user'] = user1

        return attrs


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

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
        label=_("ایمیل"),
        write_only=True
    )

    password = serializers.CharField(
        label=_("رمز عبور"),
        min_length=6,
        write_only=True,
        help_text=_("رمز عبور باید حداقل 6 کاراکتر باشد")
    )

    token = serializers.CharField(
        label=_("توکن"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # user = User.objects.get(email=email)
        # if user:
        #     if user.check_password(password):
        #         attrs['user'] = user
        #     else:
        #         msg = _("رمز عبور اشتباه است")
        #         raise serializers.ValidationError(msg, code= 'authorization')
        # else:
        #     msg = _("کاربر با این مشخصات وجود ندارد")
        #     raise serializers.ValidationError(msg, code= 'authorization')

        if email and password:

            if User.objects.filter(email=email, password=password).exists():
                user1 = User.objects.get(email=email)

            elif User.objects.filter(email=email).exists():
                user = User.objects.filter(email=email).first()
                msg = _("رمز عبور اشتباه است")
                raise serializers.ValidationError(msg, code='authorization')
            else:
                msg = _("کاربر با این مشخصات وجود ندارد")
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _("اطلاعات کابر باید به درستی و کامل وارد شود")
            raise serializers.ValidationError(msg, code='authorization')

        if user1:
            attrs['user'] = user1

        return attrs


class VerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['otp']


class RestPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp_token = serializers.CharField(required=True)
    password1 = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        user = User.objects.filter(email=email).first()
        if User.objects.filter(email=email).exists():
            if password1 != password2:
                msg = _("لطفا هردو گذرواژه را یکسان وارد نمایید")
                raise serializers.ValidationError(msg, code='conflict')
            otp = attrs.get('otp_token')
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
            msg = _("کاربری با این اطلاعات وجود ندارد")
            raise serializers.ValidationError(msg, code='authorization')


class CityListSerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']
        read_only_fields = ['id']


class UserSerializer(serializers.ModelSerializer):
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all(), many=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'gender', 'email', 'birth_date', 'city', 'avatar',
                  'mobile_number', 'bio', 'score']
        read_only_fields = ['email']

    def validate(self, attrs):
        if attrs['username']:
            username = attrs.get('username')
            if User.objects.filter(username=username).exists():
                msg = _("کاربر با این نام کاربری وجود دارد")
                raise serializers.ValidationError(msg, code='authorization')

        return attrs


# Patogh start----------------------------------------------------------------------------------

class PatoghInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatoghInfo
        fields = "__all__"


class PatoghSerializer(serializers.ModelSerializer):
    patoghinfo = PatoghInfoSerializer()

    class Meta:
        model = Patogh
        fields = "__all__"


class PatoghInfoLimitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatoghInfo
        fields = ('name', 'city')


class PatoghLimitSerializer(serializers.ModelSerializer):
    patoghinfo = PatoghInfoLimitedSerializer()

    class Meta:
        model = Patogh
        fields = ('id', 'start_time', 'patoghinfo')


class PatoghSerializerCalledByInfo(serializers.ModelSerializer):
    class Meta:
        model = Patogh
        fields = "__all__"


class PatoghHaveImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatoghHaveImages
        fields = "__all__"


class PatoghMembersSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatoghMembers
        fields = "__all__"


class PatoghAndOtherModelSerializer(serializers.ModelSerializer):
    patogh = PatoghSerializerCalledByInfo()
    patoghhaveimages = PatoghHaveImagesSerializer()
    patoghmembers = PatoghMembersSerializer()

    class Meta:
        model = PatoghInfo
        fields = '__all__'

    def create(self, validated_data):
        patogh = validated_data.pop('patogh')
        patoghhaveimages = validated_data.pop('patoghhaveimages')
        patoghmembers = validated_data.pop('patoghmembers')
        patoghinfo = super().create(validated_data)
        print(patoghinfo + "asfdsajdflasbfoahsfohasfas;iugsafiuvasfi")
        Patogh.objects.create(patogh_id=patoghinfo['id'], **patogh)
        PatoghHaveImages.objects.create(patogh_id=patoghinfo, **patoghhaveimages)
        PatoghMembers.objects.create(patogh_id=patoghinfo, **patoghmembers)

        return patoghinfo

    def update(self, instance, validated_data):
        patoghs_data = validated_data.pop('patogh')
        patoghhaveimages_data = validated_data.pop('patoghhaveimages')
        patoghmembers_data = validated_data.pop('patoghmembers')

        patoghs = (instance.patogh).all()
        patoghs = list(patoghs)

        patoghhaveimages = (instance.patoghhaveimages).all()
        patoghhaveimages = list(patoghhaveimages)

        patoghmemberss = (instance.patoghmembers).all()
        patoghmemberss = list(patoghmemberss)

        instance.name = validated_data.get('name', instance.name)
        instance.profile_image = validated_data.get('profile_image', instance.profile_image)
        instance.description = validated_data.get('description', instance.description)
        instance.type = validated_data.get('type', instance.type)
        instance.creation_time = validated_data.get('creation_time', instance.creation_time)
        instance.address = validated_data.get('address', instance.address)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.city_id = validated_data.get('city_id', instance.city_id)
        instance.creator_id = validated_data.get('creator_id', instance.creator_id)
        instance.save()

        for patogh_data in patoghs_data:
            patogh = patoghs.pop(0)
            patogh.start_time = patogh_data.get('start_time', patogh.start_time)
            patogh.end_time = patogh_data.get('end_time', patogh.end_time)
            patogh.save()

        for patoghhaveimage_data in patoghhaveimages_data:
            patoghhaveimage = patoghhaveimages.pop(0)
            patoghhaveimage.image_url = patoghhaveimage_data.get('image_url', patoghhaveimage.image_url)
            patoghhaveimage.status = patoghhaveimage_data.get('status', patoghhaveimage.status)
            patoghhaveimage.send_time = patoghhaveimage_data.get('send_time', patoghhaveimage.send_time)
            patoghhaveimage.save()

        for patoghmember_data in patoghmembers_data:
            patoghmembers = patoghmemberss.pop(0)
            patoghmembers.state = patoghmember_data.get('state', patoghmembers.state)
            patoghmembers.time = patoghmember_data.get('time', patoghmembers.time)
            patoghmembers.email_id = patoghmember_data.get('email_id', patoghmembers.email_id)
            patoghmembers.save()

        return instance


# Patogh end ----------------------------------------------------------------------------------


class UserPartiesSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    name = serializers.ReadOnlyField(source='Party.name')
    description = serializers.ReadOnlyField(source='Party.description')
    avatar = serializers.ReadOnlyField(source='Party.avatar')

    class Meta:
        model = PartyMembers
        fields = ('id', 'name', 'description', 'avatar')


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    receiver = serializers.ReadOnlyField(source='receiver.username')

    class Meta:
        model = FriendRequest
        fields = ('sender', 'receiver', 'datetime')


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'bio')



# class PatoghInfoListCreateSerializer(serializers.ModelSerializer):
#     patogh = PatoghSerializerCalledByInfo()
#     patoghhaveimages = PatoghHaveImagesSerializer()
#     patoghmembers = PatoghMembersSerializer()

# class Meta:
#     model = PatoghInfo
#     fields = '__all__'
#     read_only_fields = ['id', 'creator']

# def create(self, validated_data):
#     user = self.context['request'].user
#     id = validated_data['id']
#     patogh = validated_data.pop('patogh')
#     patoghhaveimages = validated_data.pop('patoghhaveimages')
#     patoghmembers = validated_data.pop('patoghmembers')
#     validated_data['creator'] = user
#     patoghinfo = super().create(validated_data)
#     Patogh.objects.create(patogh_id=id, **patogh)
#     PatoghHaveImages.objects.create(patogh_id=id, **patoghhaveimages)
#     PatoghMembers.objects.create(patogh_id=id, **patoghmembers)

# return patoghinfo

# def update(self, instance, validated_data):
#     status = validated_data.get('status', None)
#     if status:
#         instance.status = status
#         instance.save()
#     return instance
