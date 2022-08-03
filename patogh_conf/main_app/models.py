from django.contrib.auth.base_user import BaseUserManager
from django.db import models
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


gender_status = (
    ('female', 'زن'),
    ('male', 'مرد'),
)

province_choices = [
    ('azr-e', 'آذربایجان شرقی'),
    ('azr-w', 'آذربایجان غربی'),
    ('ardabil', 'اردبیل'),
    ('esfahan', 'اصفهان'),
    ('alborz', 'البرز'),
    ('ilam', 'ایلام'),
    ('bushehr', 'بوشهر'),
    ('tehran', 'تهران'),
    ('charmahal', 'چهارمحال و بختیاری'),
    ('khor-s', 'خراسان جنوبی'),
    ('khor-n', 'خراسان شمالی'),
    ('khor-r', 'خراسان رضوی'),
    ('khuzestan', 'خوزستان'),
    ('zanjan', 'زنجان'),
    ('semnan', 'سمنان'),
    ('sistan', 'سیستان و بلوچستان'),
    ('fars', 'فارس'),
    ('qazvin', 'قزوین'),
    ('qom', 'قم'),
    ('kordestan', 'کردستان'),
    ('kerman', 'کرمان'),
    ('kermanshah', 'کرمانشاه'),
    ('kohgiloye', 'کهگیلویه و بویر احمد'),
    ('golestan', 'گلستان'),
    ('gilan', 'گیلان'),
    ('lorestan', 'لرستان'),
    ('mazandaran', 'مازندران'),
    ('markazi', 'مرکزی'),
    ('hormozgan', 'هرمزگان'),
    ('hamedan', 'همدان'),
    ('yazd', 'یزد')
]


class User(AbstractUser):
    username = models.CharField(verbose_name=_("نام کاربری"), max_length=100, unique=True)
    first_name = models.CharField(verbose_name=_("نام"), max_length=100, null=True, blank=True)
    last_name = models.CharField(verbose_name=_("نام خانوادگی"), max_length=100, null=True, blank=True)
    email = models.EmailField(verbose_name=_("ایمیل"), max_length=50, unique=True)
    birth_date = models.DateField(verbose_name=_("تاریخ تولد"), null=True, blank=True)
    province = models.CharField(max_length=20, choices=province_choices, verbose_name='استان', null=True, blank=True)
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


class FriendRequest(models.Model):
    sender = models.ForeignKey(User, verbose_name='فرستنده', related_name='sender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, verbose_name='گیرنده', related_name='receiver', on_delete=models.CASCADE)
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
    ('male', 'پسر'),
    ('female', 'دختر'),
    ('both', 'مختلط')
]

status_choices = [
    ('private', 'خصوصی'),
    ('public', 'عمومی')
]

type_choices = [
    ('scientific', 'علمی'),
    ('athletic', 'ورزشی'),
    ('artistic', 'هنری')
]

place_choices = [
    ('park', 'پارک'),
    ('museum', 'موزه'),
    ('cafe', 'کافه'),
    ('restaurant', 'رستوران '),
    ('cinema', 'سینما')
]

repeat_choices = [
    ('none', 'هیچکدام'),
    ('weekly', 'هر هفته'),
    ('monthly', 'هر ماه')
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
    status = models.CharField(max_length=7, choices=status_choices, verbose_name='وضعیت')
    min_age = models.PositiveIntegerField(validators=[MinValueValidator(12), MaxValueValidator(50)],
                                          verbose_name='حداقل سن', null=True, blank=True)
    max_age = models.PositiveIntegerField(validators=[MinValueValidator(16), MaxValueValidator(70)],
                                          verbose_name='حداکثر سن', null=True, blank=True)
    price = models.PositiveIntegerField(verbose_name='هزینه', null=True, blank=True)
    type = models.CharField(verbose_name='نوع پاتوق', max_length=30, choices=type_choices, null=True, blank=True)
    place = models.CharField(verbose_name='مکان', choices=place_choices, max_length=40, null=True, blank=True)
    is_over = models.BooleanField(verbose_name='تمام شده', default=False)
    duration = models.PositiveIntegerField(verbose_name='مدت برگزاری',
                                           validators=[MinValueValidator(1), MaxValueValidator(10)], blank=True,
                                           null=True)
    repeat = models.CharField(verbose_name='تکرار', choices=repeat_choices, default='n', max_length=7, null=True,
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

    class Meta:
        verbose_name = 'درخواست افزودن به پاتوق'
        verbose_name_plural = 'درخواست های افزودن به پاتوق'


class HangoutRequests(models.Model):
    hangout = models.ForeignKey(Hangout, verbose_name='پاتوق', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, verbose_name='فرستنده', on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='زمان ارسال')

    class Meta:
        ordering = ['datetime']
        unique_together = ('hangout', 'sender')
        verbose_name = _('درخواست اضافه شدن به پاتوق')
        verbose_name_plural = _('درخواست های اضافه شدن به پاتوق')
