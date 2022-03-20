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


def hangout_image_profile_directory_path(instance, filename):
    return 'hangout/{0}/hangout_image/{1}'.format(str(instance.id), filename)


def patogh_image_directory_path(instance, filename):
    return 'patogh/{0}/patogh_image/{1}'.format(str(instance.id), filename)


class City(models.Model):
    name = models.CharField(max_length=50, verbose_name=_("شهر"))

    class Meta:
        ordering = ['id']
        verbose_name = _('شهر')
        verbose_name_plural = _('شهر ها')

    def __str__(self):
        return self.name


gender_status = (
    ('f', 'female'),
    ('m', 'male'),
)


class User(AbstractUser):
    username = models.CharField(verbose_name=_("نام کاربری"), max_length=100, unique=True)
    first_name = models.CharField(verbose_name=_("نام"), max_length=100, null=True, blank=True)
    last_name = models.CharField(verbose_name=_("نام خانوادگی"), max_length=100, null=True, blank=True)
    email = models.EmailField(verbose_name=_("ایمیل"), max_length=50, unique=True)
    birth_date = models.DateField(verbose_name=_("تاریخ تولد"), null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT, null=True, verbose_name=_("شهر"), blank=True)

    gender = models.CharField(verbose_name=_("جنسیت"), max_length=6, choices=gender_status, null=True,
                              blank=True)
    avatar = models.ImageField(verbose_name=_("عکس پروفایل"), upload_to=user_image_profile_directory_path
                               , null=True, blank=True, help_text=_("JPG, JPEG or PNG is validate"),
                               validators=[FileExtensionValidator(VALID_IMAGE_FORMAT), validate_image_size]
                               )
    friends = models.ManyToManyField('User', verbose_name='دوستان', blank=True)
    bio = models.CharField(verbose_name=_("بیو"), max_length=1000, null=True, blank=True)
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
    send_time = models.DateTimeField(verbose_name=_("زمان ارسال"), auto_now_add=True)
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


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name='نام')
    description = models.CharField(max_length=200, verbose_name='توضیحات', blank=True, null=True)
    creator = models.ForeignKey(User, verbose_name='سازنده', on_delete=models.CASCADE, related_name='creator')
    date = models.DateField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    members = models.ManyToManyField(User, blank=True, verbose_name='اعضا')
    photo = models.ImageField(verbose_name="عکس اکیپ",
                              upload_to=party_image_profile_directory_path,
                              null=True, blank=True, help_text=_("JPG, JPEG or PNG is validate"),
                              validators=[FileExtensionValidator(VALID_IMAGE_FORMAT), validate_image_size])

    class Meta:
        ordering = ['-date']
        verbose_name = 'اکیپ'
        verbose_name_plural = 'اکیپ ها'


hangout_gender_choices = [
    ('m', 'پسر'),
    ('f', 'دختر'),
    ('b', 'مختلط')
]

status_choices = [
    ('pr', 'خصوصی'),
    ('pu', 'عمومی')
]

province_choices = [
    ('ea', 'آذربایجان شرقی'),
    ('wa', 'آذربایجان غربی'),
    ('ard', 'اردبیل'),
    ('esf', 'اصفهان'),
    ('alb', 'البرز'),
    ('ila', 'ایلام'),
    ('bus', 'بوشهر'),
    ('teh', 'تهران'),
    ('cha', 'چهارمحال و بختیاری'),
    ('khs', 'خراسان جنوبی'),
    ('khn', 'خراسان شمالی'),
    ('khr', 'خراسان رضوی'),
    ('khu', 'خوزستان'),
    ('zan', 'زنجان'),
    ('sem', 'سمنان'),
    ('sis', 'سیستان و بلوچستان'),
    ('far', 'فارس'),
    ('qaz', 'قزوین'),
    ('qom', 'قم'),
    ('kor', 'کردستان'),
    ('ker', 'کرمان'),
    ('kermanshah', 'کرمانشاه'),
    ('koh', 'کهگیلویه و بویر احمد'),
    ('gol', 'گلستان'),
    ('gil', 'گیلان'),
    ('lor', 'لرستان'),
    ('maz', 'مازندران'),
    ('mar', 'مرکزی'),
    ('hor', 'هرمزگان'),
    ('ham', 'همدان'),
    ('yazd', 'یزد')

]

type_choices = [
    ('e', 'علمی'),
    ('v', 'ورزشی'),
    ('a', 'هنری')
]

place_choices = [
    ('p', 'پارک'),
    ('m', 'موزه'),
    ('c', 'کافه'),
    ('r', 'رستوران '),
    ('c', 'سینما')
]

repeat_choices = [
    ('n', 'هیچکدام'),
    ('w', 'هر هفته'),
    ('m', 'هر ماه')
]


class Hangout(models.Model):
    name = models.CharField(max_length=30, verbose_name='نام')
    datetime = models.DateTimeField(verbose_name='زمان برگذاری')
    description = models.CharField(max_length=100, verbose_name='توضیحات')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='سازنده', related_name='hangout_creator')
    address = models.CharField(verbose_name='آدرس', max_length=300)
    gender = models.CharField(max_length=10, choices=hangout_gender_choices, verbose_name='جنسیت')
    province = models.CharField(max_length=20, choices=province_choices, verbose_name='استان')
    members = models.ManyToManyField(User, verbose_name='اعضا')
    status = models.CharField(max_length=2, choices=status_choices, verbose_name='وضعیت')
    min_age = models.PositiveIntegerField(validators=[MinValueValidator(12), MaxValueValidator(50)],
                                          verbose_name='حداقل سن', null=True, blank=True)
    max_age = models.PositiveIntegerField(validators=[MinValueValidator(16), MaxValueValidator(70)],
                                          verbose_name='حداکثر سن', null=True, blank=True)
    price = models.PositiveIntegerField(verbose_name='هزینه', null=True, blank=True)
    type = models.CharField(verbose_name='نوع پاتوق', max_length=30, choices=type_choices, null=True, blank=True)
    place = models.CharField(verbose_name='مکان', choices=place_choices, max_length=40, null=True, blank=True)
    is_over = models.BooleanField(verbose_name='تمام شده', default=False
                                  )
    duration = models.PositiveIntegerField(verbose_name='مدت برگزاری',
                                           validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True,
                                           null=True)
    repeat = models.CharField(verbose_name='تکرار', choices=repeat_choices, default='n', max_length=1, null=True,
                              blank=True)
    maximum_members = models.PositiveIntegerField(verbose_name='حداکثر تعداد اعضا', null=True, blank=True)

    class Meta:
        verbose_name = 'پاتوق'
        verbose_name_plural = 'پاتوق ها'


class HangoutImage(models.Model):
    image = models.ImageField(verbose_name='عکس', upload_to=hangout_image_profile_directory_path,
                              validators=[FileExtensionValidator(VALID_IMAGE_FORMAT), validate_image_size])
    hangout = models.ForeignKey(Hangout, verbose_name='پاتوق', on_delete=models.CASCADE)



class HangoutInvitation(models.Model):
    hangout = models.ForeignKey(Hangout, verbose_name='پاتوق', on_delete=models.CASCADE)
    datetime = models.DateField(verbose_name='زمان ارسال', auto_now_add=True)
    user = models.ForeignKey(User, verbose_name='کاربر', on_delete=models.CASCADE)
