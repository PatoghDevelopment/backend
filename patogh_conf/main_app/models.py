from enum import auto
from django.contrib.auth.base_user import BaseUserManager
from django.core import validators
from django.db import models, transaction
import uuid
from datetime import date
import hashlib
from django.db.models import indexes
from django.db.models.aggregates import Max
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import CharField
from django.contrib.auth.models import AbstractUser, UserManager
from django.template import defaultfilters
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator, validate_slug, MaxValueValidator, MinValueValidator, \
    FileExtensionValidator, ValidationError
from django.template.defaultfilters import default, filesizeformat
from django.contrib.auth.hashers import make_password
from django.apps import apps

from random import choice
from string import ascii_lowercase, digits


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):

        if email is None:
            raise TypeError(_('Users must have an email address.'))

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """

        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        user.password = make_password(password)
        user.save(using=self._db)
        return user


UNIDENTIFIED = '-1'
IDENTIFIED = '1'
REQUESTED = '0'

verify_state = (
    (REQUESTED, 'registered'),
    (IDENTIFIED, 'verified'),
    (UNIDENTIFIED, 'unverified'),
)


def validate_image_size(image):
    if image.size > 2097152:
        raise ValidationError('حد اکثر سایز عکس باید 2 مگابایت باشد')


VALID_IMAGE_FORMAT = ['png', 'jpg', 'jpeg']


def user_image_profile_directory_path(instance, filename):
    return 'user/{0}/prof_image/{1}'.format(str(instance.username), filename)


def dorhami_image_profile_directory_path(instance, filename):
    return 'dorhami/{0}/prof_image/{1}'.format(str(instance.patogh_id), filename)


def party_image_profile_directory_path(instance, filename):
    return 'party/{0}/prof_image/{1}'.format(str(instance.id), filename)


def patogh_image_directory_path(instance, filename):
    return 'patogh/{0}/patogh_image/{1}'.format(str(instance.id), filename)


class PatoghCategory(models.Model):
    id = models.UUIDField(verbose_name=_("شناسه"), primary_key=True, default=uuid.uuid4,
                          help_text="Unique Id for this Category")
    name = models.CharField(max_length=50, verbose_name=_("کتگوری"))

    class Meta:
        ordering = ['id']
        verbose_name = _('کتگوری')
        verbose_name_plural = _('کتگوری ها')


class LocationTypes(models.Model):
    id = models.UUIDField(verbose_name=_("شناسه"), primary_key=True, default=uuid.uuid4,
                          help_text="Unique Id for this location type")
    name = models.CharField(max_length=30, verbose_name=_("نوع مکان"))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = _('مکان')
        verbose_name_plural = _('مکان ها')


class Tags(models.Model):
    id = models.UUIDField(verbose_name=_("شناسه"), primary_key=True, default=uuid.uuid4,
                          help_text="Unique Id for this Tag")
    tag = models.CharField(verbose_name=_("برچسب"), unique=True, max_length=40)

    def __str__(self):
        return self.tag

    class Meta:
        ordering = ['id']
        unique_together = ('id', 'tag')
        verbose_name = _('برچست')
        verbose_name_plural = _('برچسب ها')


class City(models.Model):
    id = models.UUIDField(verbose_name=_("شناسه"), primary_key=True, default=uuid.uuid4,
                          help_text="Unique Id for this Tag")
    name = models.CharField(max_length=50, verbose_name=_("شهر"))

    class Meta:
        ordering = ['id']
        verbose_name = _('شهر')
        verbose_name_plural = _('شهر ها')

    def __str__(self):
        return self.name


def generate_random_username(length=16, chars=ascii_lowercase + digits, split=4, delimiter='-'):
    username = ''.join([choice(chars) for i in range(length)])

    if split:
        username = delimiter.join([username[start:start + split] for start in range(0, len(username), split)])

    try:
        User.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
    except User.DoesNotExist:
        return username;


class User(AbstractUser):
    username = models.CharField(verbose_name=_("نام کاربری"), max_length=100, unique=True,
                                default=generate_random_username)
    first_name = models.CharField(verbose_name=_("نام"), max_length=100, null=True, blank=True)
    last_name = models.CharField(verbose_name=_("نام خانوادگی"), max_length=100, null=True, blank=True)
    email = models.EmailField(verbose_name=_("ایمیل"), max_length=50, primary_key=True)
    mobile_number = models.CharField(verbose_name=_("شماره تلفن"), unique=True, max_length=12, null=True, blank=True)
    birth_date = models.DateField(verbose_name=_("تاریخ تولد"), null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True, verbose_name=_("شهر"), blank=True)
    gender_status = (
        ('0', 'female'),
        ('1', 'male')
    )
    gender = models.CharField(verbose_name=_("جنسیت"), max_length=6, choices=gender_status, default='1', null=True,
                              blank=True)
    avatar = models.ImageField(verbose_name=_("عکس پروفایل"), upload_to=user_image_profile_directory_path
                               , null=True, blank=True, help_text=_("JPG, JPEG or PNG is validate"),
                               validators=[FileExtensionValidator(VALID_IMAGE_FORMAT), validate_image_size]
                               )
    bio = models.CharField(verbose_name=_("درباره"), max_length=1000, null=True, blank=True)
    score = models.IntegerField(verbose_name=_("امتیاز کاربر"), null=True, blank=True, default=0)
    parties = models.ManyToManyField("Party", through="PartyMembers", blank=True)

    objects = UserManager()
    friends = models.ManyToManyField('User', verbose_name='دوستان', blank=True)

    def __str__(self):
        return self.username

    class Meta:
        ordering = ['username']
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')


class PendingVerify(models.Model):
    receptor = models.EmailField(verbose_name=_("دریافت کننده"), primary_key=True, max_length=50, default='a@a.com')
    otp = models.IntegerField(verbose_name=_("OTP کد"))
    send_time = models.DateTimeField(verbose_name=_("زمان ارسال"), auto_now_add=True, blank=True, null=True)
    allowed_try = models.SmallIntegerField(verbose_name=_(" دفعات مجاز برای تلاش"), default=5
                                           , validators=[MinValueValidator(0), MaxValueValidator(5)])
    objects = models.Manager()

    def __str__(self):
        return self.receptor

    class Meta:
        ordering = ['send_time']
        verbose_name = _('تاییدیه')
        verbose_name_plural = _('تاییدیه ها')


class Party(models.Model):
    id = models.UUIDField(primary_key=True, verbose_name=_("شناسه"), default=uuid.uuid4,
                          help_text="Unique Id for this party")
    name = models.CharField(verbose_name=_("نام"), max_length=128, null=True, blank=True)
    avatar = models.ImageField(verbose_name=_("عکس اکیپ"),
                               upload_to=party_image_profile_directory_path,
                               null=True, blank=True, help_text=_("JPG, JPEG or PNG is validate"),
                               validators=[FileExtensionValidator(VALID_IMAGE_FORMAT), validate_image_size])
    creator = models.ForeignKey(User, verbose_name=_("پدید آورنده"), on_delete=models.PROTECT, null=True)
    description = models.CharField(verbose_name=_("توضیحات"), help_text="descripe your party", max_length=1000)
    creation_time = models.DateTimeField(verbose_name=_("زمان ساخت اکیپ"), help_text="Creation time for the party",
                                         auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = _('اکیپ')
        verbose_name_plural = _('اکیپ ها')


class PatoghInfo(models.Model):
    id = models.UUIDField(primary_key=True, verbose_name=_("شناسه"), default=uuid.uuid4,
                          help_text="Unique Id for this gathering")
    creator = models.ForeignKey(User, verbose_name=_("شناسه پدید آورنده"), on_delete=models.PROTECT, null=True,
                                blank=True)
    name = models.CharField(verbose_name=_("نام"), max_length=50, null=True, blank=True)
    profile_image = models.ImageField(verbose_name=_("عکس پاتوق"),
                                      upload_to=patogh_image_directory_path,
                                      null=True, blank=True, help_text=_("JPG, JPEG or PNG is validate"),
                                      validators=[FileExtensionValidator(VALID_IMAGE_FORMAT), validate_image_size])
    city = models.ForeignKey(City, verbose_name=_("شهر"), on_delete=models.PROTECT, null=True, blank=True)
    description = models.CharField(verbose_name=_("توضیحات"), help_text="descripe your patogh", max_length=1000)
    state = (
        ('0', 'public'),
        ('1', 'private')
    )
    type = models.CharField(verbose_name=_("حالت دورهمی"), default='0', choices=state, max_length=10)
    creation_time = models.DateTimeField(verbose_name=_("زمان ساخت پاتوق"), help_text="Creation time for the patogh",
                                         auto_now_add=True, null=True)
    category = models.ForeignKey(PatoghCategory, verbose_name=_("نوع پاتوق"), on_delete=models.PROTECT, null=True,
                                 blank=True)
    address = models.CharField(verbose_name=_("آدرس"), max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = _('اطلاعات دورهمی')
        verbose_name_plural = _('اطلاعات دورهمی ها')


class Patogh(models.Model):
    id = models.UUIDField(primary_key=True, verbose_name=_("شناسه"), default=uuid.uuid4,
                          help_text="Unique Id for this gathering")
    patogh_id = models.ForeignKey(PatoghInfo, verbose_name=_("شناسه اطلاعات پاتوق"), on_delete=models.PROTECT,
                                  null=True)
    start_time = models.DateTimeField(verbose_name=_("زمان شروع"), help_text="Start time for the patogh", null=True)
    end_time = models.DateTimeField(verbose_name=_("زمان پایان"), help_text="end time for the patogh", null=True)

    def __str__(self):
        return self.id

    @transaction.atomic
    def save(self, *args, **kwargs):
        if not hasattr(self, "patogh_id"):
            self.patogh_id, _ = PatoghInfo.objects.get_or_create(id=self.id)

        super(Patogh, self).save(*args, **kwargs)

    # def create_patogh_patoghinfo(instance, created, raw, **kwargs):
    #     # Ignore fixtures and saves for existing courses.
    #     if not created or raw:
    #         return

    #     if not instance.patogh_id_id:
    #         group, _ = PatoghInfo.objects.get_or_create(name='_course_' + self.id + '_student')
    #         instance.student_group = group

    #     if not instance.teacher_group_id:
    #         teacher_group, _ = Group.objects.get_or_create(name='_course_' + self.id + '_teacher')
    #         instance.teacher_group = teacher_group

    #     instance.save()

    # models.signals.post_save.connect(create_course_groups, sender=Course, dispatch_uid='create_course_groups')
    # @transaction.atomic
    # def save(self, *args, **kwargs):
    #     if not self.patogh_id_id:
    #         self.patogh_id, _ = PatoghInfo.objects.get_or_create(id= self.id)

    #     super(Patogh, self).save(*args, **kwargs)

    class Meta:
        ordering = ['id']
        verbose_name = _('دورهمی')
        verbose_name_plural = _('دورهمی ها')


class PartyMembers(models.Model):
    p_id = models.ForeignKey(Party, verbose_name=_("اکیپ"), on_delete=models.PROTECT)
    g_id = models.ForeignKey(User, verbose_name=_("کاربر"), on_delete=models.PROTECT)
    is_admin = (
        ('0', 'no'),
        ('1', 'yes')
    )
    status = models.SmallIntegerField(verbose_name=_("سطح دسترسی کاربر به اکیپ"), choices=is_admin, default='0')

    class Meta:
        unique_together = (("p_id", "g_id"))
        ordering = ['p_id']
        verbose_name = _('عضو اکیپ')
        verbose_name_plural = _('اعضای اکیپ')

    def __str__(self):
        return self.username.username


class PatoghMembers(models.Model):
    patogh_id = models.ForeignKey(PatoghInfo, verbose_name=_("شناسه پاتوق"), on_delete=models.PROTECT, null=True)
    email = models.ForeignKey(User, verbose_name=_("شناسه کاربر"), on_delete=models.PROTECT, null=True)
    status = (
        ('0', 'admin'),
        ('1', 'normal participant')
    )
    state = models.CharField(verbose_name=_("مجوز کاربر"), choices=status, help_text="سطح دسترسی کاربر را مشخص کنید",
                             default='1', max_length=10)
    time = models.DateTimeField(verbose_name=_("زمان پیوستن"), help_text="attend patogh time", auto_now_add=True)

    def __str__(self):
        return self.patogh_id + " " + self.email

    class Meta:
        ordering = ['patogh_id']
        verbose_name = _('عضو دورهمی')
        verbose_name_plural = _('اعضای دورهمی')


class PatoghsComments(models.Model):
    id = models.UUIDField(verbose_name=_("شناسه"), primary_key=True, default=uuid.uuid4,
                          help_text="Unique Id for this patogh Commments")
    sender = models.ForeignKey(User, verbose_name=_("فرستنده"), on_delete=models.PROTECT, null=True)
    patogh_id = models.ForeignKey(Patogh, verbose_name=_("شناسه پاتوق"), on_delete=models.PROTECT, null=True)
    reply_to = models.ForeignKey('self', verbose_name=_("بازخورد به"), on_delete=models.CASCADE)
    send_time = models.DateTimeField(verbose_name=_("زمان ارسال"), auto_now_add=True, blank=True)
    comment = models.CharField(verbose_name=_("نظر"), max_length=1000)

    def __str__(self):
        return self.id + " has commented " + self.comment

    class Meta:
        ordering = ['id']
        verbose_name = _('نظر در مورد پاتوق')
        verbose_name_plural = _('نظرات در مورد پاتوق')


class reportedPatogh(models.Model):
    patogh_id = models.ForeignKey(Patogh, verbose_name=_("شناسه پاتوق"), on_delete=models.PROTECT)
    username = models.ForeignKey(User, verbose_name=_("نام کاربری"), on_delete=models.PROTECT)
    massage = models.CharField(verbose_name=_("پیام"), max_length=1000)
    send_time = models.DateTimeField(verbose_name=_("زمان ارسال"), auto_now_add=True, blank=True)

    def __str__(self):
        return self.patogh_id

    class Meta:
        ordering = ['patogh_id']
        unique_together = ('patogh_id', 'username')
        verbose_name = _('پاتوق گزارش شده')
        verbose_name_plural = _('پاتوق های گزارش شده')


class PatoghHaveImages(models.Model):
    patogh_id = models.ForeignKey(Patogh, verbose_name=_("شناسه پاتوق"), on_delete=models.CASCADE)
    image_url = models.ImageField(verbose_name=_("عکس برای دورهمی"),
                                  upload_to=dorhami_image_profile_directory_path,
                                  null=True, blank=True, help_text=_("JPG, JPEG or PNG is validate"),
                                  validators=[FileExtensionValidator(VALID_IMAGE_FORMAT), validate_image_size])
    state = (
        (0, 'registered'),
        (1, 'accepted'),
        (2, 'rejected'),
        (3, 'deleted')
    )
    status = models.SmallIntegerField(verbose_name=_("وضعیت تایید عکس"), choices=state, default=0)
    send_time = models.DateTimeField(verbose_name=_("زمان ارسال"), auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.patogh_id + " has " + self.state

    class Meta:
        ordering = ['patogh_id']
        verbose_name = _('عکس پاتوق')
        verbose_name_plural = _('عکس های پاتوق')


class UsersHaveFriends(models.Model):
    sender = models.ForeignKey(User, related_name='sender_set', on_delete=models.PROTECT, verbose_name=_("فرستنده"))
    receiver = models.ForeignKey(User, related_name='reciver_set', on_delete=models.PROTECT, verbose_name=_("گیرنده"))
    status = (
        (0, 'rejected'),
        (1, 'pending answer'),
        (2, 'accepted')
    )
    state = models.SmallIntegerField(verbose_name=_("وضعیت دوستی"), default=1, choices=status)
    time = models.DateTimeField(verbose_name=_("زمان درخواست دوستی"), auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.sender + " requested to: " + self.receiver

    class Meta:
        ordering = ['time']
        unique_together = ('sender', 'receiver')
        verbose_name = _('وضعیت درخواست')
        verbose_name_plural = _('وضعیت درخواست ها')


STATUS_CHOICES = [
    ('a', 'پاسخ داده شده'),
    ('w', 'در انتظار')
]


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, verbose_name='فرستنده', related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, verbose_name='گیرنده', related_name='receiver', on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name='وضعیت', null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')

    class Meta:
        ordering = ['-datetime']
        verbose_name = 'درخواست دوستی'
        verbose_name_plural = 'درخواست های دوستی'
