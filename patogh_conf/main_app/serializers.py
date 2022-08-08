from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import datetime


class SignupOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(label='ایمیل', write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')

        if email:
            if User.objects.filter(email=email).exists():
                msg = _("کاربر با این مشخصات وجود دارد")
                raise serializers.ValidationError(msg, code='authorization')
        else:
            raise serializers.ValidationError('ایمیل نمی تواند خالی باشد!', code='authorization')
        return attrs


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField(label='ایمیل', write_only=True)
    username = serializers.CharField(label=_("نام کاربری"), max_length=100, write_only=True)
    otp = serializers.CharField(label=_("کد تایید"), write_only=True)
    password1 = serializers.CharField(label=_("رمز عبور"), min_length=6, max_length=30,
                                      write_only=True, help_text=_("رمز عبور باید حداقل 6 کاراکتر باشد"))
    password2 = serializers.CharField(label=_("تایید رمز عبور"), min_length=6, max_length=30,
                                      write_only=True, help_text=_("رمز عبور باید حداقل 6 کاراکتر باشد"))

    def validate(self, attrs):
        email = attrs.get('email')
        username = attrs.get('username')
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if email and username and password1 and password2:
            if User.objects.filter(email=email).exists():
                msg = _("کاربر با این مشخصات وجود دارد")
                raise serializers.ValidationError(msg, code='conflict')
            elif User.objects.filter(username=username).exists():
                msg = _("این نام کاربری موجود است")
                raise serializers.ValidationError(msg, code='conflict')
            elif password1 != password2:
                msg = _("لطفا هردو گذرواژه را یکسان وارد نمایید")
                raise serializers.ValidationError(msg, code='conflict')
            else:
                otp = attrs.get('otp')
                pending_verify_obj = PendingVerify.objects.filter(receptor=email).first()
                time_now = timezone.now()
                if time_now < pending_verify_obj.send_time + datetime.timedelta(minutes=5):
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
        username = validated_data['username']
        password1 = validated_data['password1']
        user = User.objects.create_user(email, username, password1)
        PendingVerify.objects.filter(receptor=email).delete()
        return user


class SigninSerializer(serializers.Serializer):
    email = serializers.CharField(label=_("ایمیل یا نام کاربری"), write_only=True)
    password = serializers.CharField(label=_("رمز عبور"), min_length=6, write_only=True,
                                     help_text=_("رمز عبور باید حداقل 6 کاراکتر باشد"))
    token = serializers.CharField(label="توکن", read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        if email and password:
            if User.objects.filter(email=email):
                user = authenticate(request=self.context.get('request'),
                                    email=email, password=password)
                if not user:
                    raise serializers.ValidationError('ایمیل ،نام کاربری یا رمز عبور اشتباه است!')
                attrs['user'] = user
            elif User.objects.filter(username=email):
                user1 = User.objects.filter(username=email).first()
                user = authenticate(request=self.context.get('request'),
                                    username=user1.email, password=password)
                if not user:
                    raise serializers.ValidationError('ایمیل ،نام کاربری یا رمز عبور اشتباه است!')
                attrs['user'] = user
            else:
                raise serializers.ValidationError('ایمیل ،نام کاربری یا رمز عبور اشتباه است!')
        else:
            raise serializers.ValidationError('اطلاعات را به درستی وارد کنید!', code='authorization')
        return attrs


class VerifyOTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['otp']


class ForgotPasswordSendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(label='ایمیل', write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        if email:
            user = User.objects.filter(email=email)
            if user:
                user = user.first()
            if not user:
                raise serializers.ValidationError('کاربری با این اطلاعات موجود نیست!', code='authorization')
        else:
            raise serializers.ValidationError('ایمیل نمی تواند خالی باشد!', code='authorization')
        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(label='ایمیل', write_only=True)
    otp = serializers.CharField(label=_("کد تایید"), write_only=True)
    password1 = serializers.CharField(label=_("رمز عبور"), min_length=6, max_length=30,
                                      write_only=True, help_text=_("رمز عبور باید حداقل 6 کاراکتر باشد"))
    password2 = serializers.CharField(label=_("تایید رمز عبور"), min_length=6, max_length=30,
                                      write_only=True, help_text=_("رمز عبور باید حداقل 6 کاراکتر باشد"))
    token = serializers.CharField(label="توکن", read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password1 = attrs.get('password1')
        password2 = attrs.get('password2')
        if email and password1 and password2:
            if User.objects.filter(email=email):
                if password1 != password2:
                    raise serializers.ValidationError('لطفا هردو گذرواژه را یکسان وارد نمایید', code='conflict')
                otp = attrs.get('otp')
                pending_verify_obj = PendingVerify.objects.filter(receptor=email).first()
                time_now = timezone.now()
                if time_now < pending_verify_obj.send_time + datetime.timedelta(minutes=5):
                    if int(otp) == pending_verify_obj.otp:
                        return attrs
                    else:
                        raise serializers.ValidationError("کد تایید وارد شده اشتباه است.")
                else:
                    raise serializers.ValidationError("کد تایید منقضی شده است.")
            else:
                raise serializers.ValidationError('کاربری با این اطلاعات وجود ندارد', code='authorization')
        else:
            raise serializers.ValidationError('اطلاعات را به درستی وارد کنید!', code='authorization')


class UserSerializer(serializers.ModelSerializer):
    is_friend = serializers.SerializerMethodField()
    num_of_friends = serializers.SerializerMethodField()
    num_of_companies = serializers.SerializerMethodField()
    hangouts_in_common = serializers.SerializerMethodField()
    num_of_hangouts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'gender', 'email', 'birth_date', 'province', 'avatar', 'bio',
                  'is_friend', 'num_of_friends', 'num_of_companies', 'hangouts_in_common', 'num_of_hangouts']
        read_only_fields = ['email']

    def get_is_friend(self, user):
        if self.context.get('request').user.friends.filter(email=user.email).exists():
            return True
        return False

    def get_hangouts_in_common(self, friend):
        a = Hangout.objects.filter(members__in=[friend])
        b = Hangout.objects.filter(members__in=[self.context['request'].user])
        c = []
        for i in a:
            for j in b:
                if j == i:
                    c.append(j)
        k = 0
        for i in c:
            k += 1
        return k

    def get_num_of_friends(self, user):
        return user.friends.count()

    def get_num_of_companies(self, user):
        return user.company_set.count()

    def get_num_of_hangouts(self, user):
        return user.hangout_set.count()


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(label='رمز عبور قبلی', max_length=128, required=True,
                                         write_only=True)
    new_password = serializers.CharField(label=_("رمز عبور جدید"), min_length=6, max_length=30,
                                         write_only=True, help_text=_("رمز عبور باید حداقل 6 کاراکتر باشد"))
    new_password_confirmation = serializers.CharField(label=_("تایید رمز عبور جدید"), min_length=6, max_length=30,
                                                      write_only=True,
                                                      help_text=_("رمز عبور باید حداقل 6 کاراکتر باشد"))

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('رمز عبور قبلی اشتباه است!')
        return value

    def validate(self, data):
        if data['new_password'] == data['old_password']:
            raise serializers.ValidationError('رمز عبور قبلی و جدید یکسان است!', code='conflict')
        if data['new_password'] != data['new_password_confirmation']:
            raise serializers.ValidationError('رمز عبور با تکرارش یکسان نیست!', code='conflict')
        return data

    def save(self, **kwargs):
        password = self.validated_data['new_password']
        user = self.context['request'].user
        user.set_password(password)
        user.save()
        return user


class ChangeEmailOTPSerializer(serializers.Serializer):
    new_email = serializers.EmailField(label='ایمیل جدید', write_only=True)

    def validate(self, attrs):
        new_email = attrs.get('new_email')
        if new_email:
            user = User.objects.filter(email=new_email)
            if user:
                raise serializers.ValidationError('ایمیل جدید از قبل موجود است!', code='conflict')
        else:
            raise serializers.ValidationError('اطلاعات را به درستی وارد کنید!', code='authorization')
        return attrs


class ChangeEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField(label='ایمیل جدید', write_only=True)
    otp = serializers.CharField(label='کد تایید', min_length=5, write_only=True)

    def validate(self, attrs):
        new_email = attrs.get('new_email')
        otp = attrs.get('otp')
        if new_email and otp:
            user = self.context['request'].user
            user1 = User.objects.filter(email=new_email)
            if user1:
                raise serializers.ValidationError('ایمیل جدید از قبل موجود است!', code='conflict')
            pending_verify_obj = PendingVerify.objects.filter(receptor=new_email).first()
            time_now = timezone.now()
            if time_now < pending_verify_obj.send_time + datetime.timedelta(minutes=5):
                if int(otp) == pending_verify_obj.otp:
                    return attrs
                else:
                    raise serializers.ValidationError(_("کد تایید وارد شده اشتباه است."))
            else:
                raise serializers.ValidationError(_("کد تایید منقضی شده است."))

        else:
            raise serializers.ValidationError('این فیلد نمی تواند خالی باشد!', code='authorization')

    def save(self, **kwargs):
        new_email = self.validated_data['new_email']
        user = self.context['request'].user
        user.email = new_email
        user.save()
        return user


class SupportSerializer(serializers.ModelSerializer):
    date = serializers.ReadOnlyField()

    class Meta:
        model = Support
        fields = ['id', 'email', 'description', 'date']


class FriendRequestSerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    receiver = serializers.ReadOnlyField(source='receiver.username')

    class Meta:
        model = FriendRequest
        fields = ('sender', 'receiver', 'datetime')


class FriendSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField()
    bio = serializers.ReadOnlyField()
    hangouts_in_common = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('username', 'bio', 'hangouts_in_common')

    def get_hangouts_in_common(self, friend):
        a = Hangout.objects.filter(members__in=[friend])
        b = Hangout.objects.filter(members__in=[self.context['request'].user])
        c = []
        for i in a:
            for j in b:
                if j == i:
                    c.append(j)
        k = 0
        for i in c:
            k += 1
        return k



class CompanySerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    num_of_members = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'photo', 'date', 'creator', 'num_of_members')

    def get_num_of_members(self, company):
        return company.members.count()


class LeaveCompanySerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField()
    description = serializers.ReadOnlyField()
    photo = serializers.ReadOnlyField()
    creator = serializers.ReadOnlyField(source='creator.username')
    num_of_members = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ('id', 'name', 'description', 'photo', 'date', 'creator', 'num_of_members')

    def get_num_of_members(self, company):
        return company.members.count()


class CompanyRUDSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    name = serializers.ReadOnlyField()
    num_of_members = serializers.SerializerMethodField()

    class Meta:
        model = Company
        fields = ['id', 'name', 'description', 'photo', 'date', 'creator', 'num_of_members']

    def get_num_of_members(self, company):
        return company.members.count()


class HangoutSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    num_of_members = serializers.SerializerMethodField()
    is_over = serializers.ReadOnlyField()
    is_creator = serializers.SerializerMethodField()

    class Meta:
        model = Hangout
        fields = ['id', 'name', 'description', 'address', 'is_over', 'duration', 'is_creator', 'repeat', 'creator',
                  'datetime',
                  'gender', 'province', 'status', 'min_age',
                  'max_age', 'type',
                  'price', 'place', 'maximum_members', 'num_of_members']

    def get_num_of_members(self, hangout):
        return hangout.members.count()

    def get_is_creator(self, hangout):
        if hangout.creator == self.context.get('request').user:
            return True
        return False


class FinishHangoutSerializer(serializers.ModelSerializer):
    creator = serializers.ReadOnlyField(source='creator.username')
    num_of_members = serializers.SerializerMethodField()

    class Meta:
        model = Hangout
        fields = ['id', 'name', 'description', 'address', 'is_over', 'duration', 'repeat', 'creator', 'datetime',
                  'gender', 'province', 'status', 'min_age',
                  'max_age', 'type',
                  'price', 'place', 'num_of_members']
        read_only_fields = ['id', 'name', 'description', 'address', 'is_over', 'duration', 'repeat', 'creator',
                            'datetime',
                            'gender', 'province', 'status', 'min_age',
                            'max_age', 'type',
                            'price', 'place', 'num_of_members']

    def get_num_of_members(self, hangout):
        return hangout.members.count()


class HangoutInvitationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='username')
    hangout = serializers.ReadOnlyField(source='hangout.name')

    class Meta:
        model = HangoutInvitation
        fields = ['id', 'user', 'hangout', 'datetime']


class HangoutRUDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hangout
        fields = ['id', 'name', 'datetime', 'description', 'address', 'gender', 'status', 'min_age', 'max_age',
                  'price', 'type', 'place', 'duration', 'maximum_members', 'repeat']


class HangoutImageSerializer(serializers.ModelSerializer):
    hangout = serializers.ReadOnlyField(source='hangout.name')

    class Meta:
        model = HangoutImage
        fields = ['id', 'hangout', 'image']


class HangoutRequestsSerializer(serializers.ModelSerializer):
    hangout = serializers.ReadOnlyField(source='hangout.name')
    sender = serializers.ReadOnlyField(source='sender.username')

    class Meta:
        model = HangoutRequests
        fields = ('id', 'hangout', 'sender', 'datetime')


class HangoutMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'gender', 'email', 'birth_date', 'province', 'avatar',
                  'bio']
        read_only_fields = ['username', 'first_name', 'last_name', 'gender', 'email', 'birth_date', 'province',
                            'avatar',
                            'bio']


class HangoutTimeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hangout
        fields = ['id', 'name', 'description', 'address', 'is_over', 'duration', 'repeat', 'creator', 'datetime',
                  'gender', 'province', 'status', 'min_age',
                  'max_age', 'type',
                  'price', 'place']
        read_only_fields = ['id', 'name', 'description', 'address', 'is_over', 'duration', 'repeat', 'creator',
                            'datetime',
                            'gender', 'province', 'status', 'min_age',
                            'max_age', 'type',
                            'price', 'place']
