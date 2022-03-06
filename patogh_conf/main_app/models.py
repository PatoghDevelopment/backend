from django.contrib.auth.base_user import BaseUserManager
from django.db import models
import uuid
from django.db.models.base import Model
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator, ValidationError


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None):

        if not email:
            raise ValueError('Users must have an email')
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=email,
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email')
        if not password:
            raise ValueError('Users must have a password')

        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
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
        raise ValidationError('حداکثر سایز عکس باید 2 مگابایت باشد')


VALID_IMAGE_FORMAT = ['png', 'jpg', 'jpeg']


def user_image_profile_directory_path(instance, filename):
    return 'user/{0}/prof_image/{1}'.format(str(instance.username), filename)


def dorhami_image_profile_directory_path(instance, filename):
    return 'dorhami/{0}/prof_image/{1}'.format(str(instance.patogh_id), filename)


def party_image_profile_directory_path(instance, filename):
    return 'party/{0}/prof_image/{1}'.format(str(instance.id), filename)


def patogh_image_directory_path(instance, filename):
    return 'patogh/{0}/patogh_image/{1}'.format(str(instance.id), filename)


class Tags(models.Model):
    id = models.UUIDField(verbose_name=_("شناسه"), primary_key=True, default=uuid.uuid4,
                          help_text="Unique Id for this Tag")
    tag = models.CharField(verbose_name=_("برچسب"), unique=True, max_length=40)

    def __str__(self):
        return self.tag

    class Meta:
        ordering = ['id']
        unique_together = ('id', 'tag')
        verbose_name = _('برچسب')
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


class User(AbstractUser):
    username = models.CharField(verbose_name=_("نام کاربری"), max_length=100, unique=True)
    first_name = models.CharField(verbose_name=_("نام"), max_length=100, null=True, blank=True)
    last_name = models.CharField(verbose_name=_("نام خانوادگی"), max_length=100, null=True, blank=True)
    email = models.EmailField(verbose_name=_("ایمیل"), max_length=50, unique=True)
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
    parties = models.ManyToManyField("Party", through="PartyMembers", blank=True)
    friends = models.ManyToManyField('User', verbose_name='دوستان', blank=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    objects = UserManager()

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


class Support(models.Model):
    email = models.EmailField(verbose_name='ایمیل')
    description = models.TextField(verbose_name='متن پیام', max_length=2000)
    date = models.DateTimeField(verbose_name='تاریخ', auto_now_add=True, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'پشتیبانی'
        verbose_name_plural = 'پشتیبانی ها'
        ordering = ['-id']


class PatoghCategory(models.Model):
    id = models.UUIDField(verbose_name=_("شناسه"), primary_key=True, default=uuid.uuid4,
                          help_text="Unique Id for this Category")
    name = models.CharField(max_length=50, verbose_name=_("کتگوری"))

    class Meta:
        ordering = ['id']
        verbose_name = _('کتگوری')
        verbose_name_plural = _('کتگوری ها')


class Patogh(models.Model):
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
    start_time = models.DateTimeField(verbose_name=_("زمان شروع"), help_text="Start time for the patogh", null=True)
    end_time = models.DateTimeField(verbose_name=_("زمان پایان"), help_text="end time for the patogh", null=True)
    category = models.ForeignKey(PatoghCategory, verbose_name=_("نوع پاتوق"), on_delete=models.PROTECT, null=True,
                                 blank=True)
    address = models.CharField(verbose_name=_("آدرس"), max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = _('پاتوق')
        verbose_name_plural = _('پاتوق ها')


class PatoghMembers(models.Model):
    patogh_id = models.ForeignKey(Patogh, verbose_name=_("شناسه پاتوق"), on_delete=models.PROTECT, null=True)
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
        verbose_name = _('عضو پاتوق')
        verbose_name_plural = _('اعضای پاتوق')


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


class PartyMembers(models.Model):
    party_id = models.ForeignKey(Party, verbose_name=_("اکیپ"), on_delete=models.PROTECT)
    member_id = models.ForeignKey(User, verbose_name=_("کاربر"), on_delete=models.PROTECT)
    is_admin = (
        ('0', 'no'),
        ('1', 'yes')
    )
    status = models.SmallIntegerField(verbose_name=_("سطح دسترسی کاربر به اکیپ"), choices=is_admin, default='0')

    class Meta:
        ordering = ['party_id']
        verbose_name = _('عضو اکیپ')
        verbose_name_plural = _('اعضای اکیپ')


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
