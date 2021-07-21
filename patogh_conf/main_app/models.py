from enum import auto
from django.contrib.auth.base_user import BaseUserManager
from django.core import validators
from django.db import models
import uuid
from datetime import date
import hashlib
from django.db.models import indexes
from django.db.models.aggregates import Max 
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import CharField
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxLengthValidator, validate_slug, MaxValueValidator, MinValueValidator, FileExtensionValidator, ValidationError
from django.template.defaultfilters import filesizeformat 
from django.contrib.auth.hashers import make_password
from django.apps import apps

class UserManager(BaseUserManager):

    def create_user(self,username, email, password=None, fullname=None,otp = None ,**kwargs):

        if fullname is None:
            raise TypeError(_('Users must have a Name'))

        if email is None:
            raise TypeError(_('Users must have an email address.'))

        user = self.model(fullname = fullname,otp = otp, username = username, email=self.normalize_email(email),**kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password,'admin','1' , **extra_fields)

    def _create_user(self, username, email, password,fullname,otp, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        GlobalUserModel = apps.get_model(self.model._meta.app_label, self.model._meta.object_name)
        username = GlobalUserModel.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.password = make_password(password)
        user.fullname = fullname
        user.otp = otp
        user.save(using=self._db)
        return user


UNIDENTIFIED = '-1'
IDENTIFIED = '1'
REQUESTED = '0'

verify_state = (
        (REQUESTED,'registered'),
        (IDENTIFIED,'verified'),
        (UNIDENTIFIED,'unverified'),        
    )

def validate_image_size(image):
    if image.size > 2097152:
        raise ValidationError('حد اکثر سایز عکس باید 2 مگابایت باشد')

VALID_IMAGE_FORMAT = ['png','jpg','jpeg']

def user_image_profile_directory_path(instance, filename):
    return 'user/{0}/prof_image/{1}'.format(str(instance.username), filename)

def dorhami_image_profile_directory_path(instance, filename):
    return 'dorhami/{0}/prof_image/{1}'.format(str(instance.patogh_id), filename)

def patogh_image_directory_path(instance, filename):
    return 'patogh/{0}/patogh_image/{1}'.format(str(instance.id), filename)

class PatoghCategory(models.Model):
    id = models.UUIDField(verbose_name=_("شناسه"),primary_key=True, default=uuid.uuid4)
    category = models.CharField(max_length=50,verbose_name=_("کتگوری"))

    class Meta: 
        ordering = ['id']
        verbose_name = _('کتگوری')
        verbose_name_plural = _('کتگوری ها')
        unique_together = ('id','category')

class LocationTypes(models.Model):
    id = models.UUIDField(verbose_name=_("شناسه") ,primary_key=True, default=uuid.uuid4,help_text="Unique Id for this Location")
    label = models.CharField(verbose_name=_("برچسب"),max_length=20 , unique=True)

    def __str__(self):
        return self.label
    class Meta:
        ordering = ['id']
        verbose_name = _('مکان')
        verbose_name_plural = _('مکان ها')


class Tags(models.Model):
    id = models.UUIDField(verbose_name=_("شناسه"),primary_key=True, default=uuid.uuid4,help_text="Unique Id for this Tag")
    tag = models.CharField(verbose_name=_("برچسب"),unique=True,max_length=40)

    def __str__(self):
        return self.tag

    class Meta:
        ordering = ['id']
        unique_together = ('id','tag')
        verbose_name = _('برچست')
        verbose_name_plural = _('برچسب ها')
        
class City(models.Model):
    id = models.UUIDField(verbose_name=_("شناسه"),primary_key=True, default=uuid.uuid4,help_text="Unique Id for this City")
    name = models.CharField(verbose_name=_("نام شهر"),max_length=40,help_text="Where do you live?")

    class Meta:
        ordering = ['name']
        unique_together = ('id','name')
        verbose_name = _('شهر')
        verbose_name_plural = _('شهر ها')
       
    def __str__(self):
        return self.name

class User(AbstractUser):
    username = models.CharField(verbose_name=_("نام کاربری"),primary_key=True,max_length=100,unique=True)
    fullname = models.CharField(verbose_name=_("نام کامل"),max_length=100,null = True , blank = True)
    email = models.EmailField(verbose_name=_("ایمیل"), max_length=50, unique=True)
    phone = models.CharField(verbose_name=_("شماره تلفن"),unique = True, max_length=12,null=True,blank=True)
    birthdate = models.DateField(verbose_name=_("تاریخ تولد"),null = True , blank = True )
    city = models.ForeignKey(City , on_delete=models.PROTECT , null = True,verbose_name=_("شهر"), blank = True)
    gender_status = (
        ('0','female'),
        ('1','male')
    )
    gender = models.CharField(verbose_name=_("جنسیت"),max_length=6,choices=gender_status,default='1',null = True ,blank=True)
    profile_image_url = models.ImageField(verbose_name=_("عکس پروفایل"),upload_to = user_image_profile_directory_path
                                          ,null = True , blank = True ,help_text =_("JPG, JPEG or PNG is validate"),
                                          validators=[FileExtensionValidator(VALID_IMAGE_FORMAT),validate_image_size]
                                          )
    bio = models.CharField(verbose_name=_("درباره"),max_length=1000,null = True , blank = True)
    otp = models.CharField(max_length=20,null=True,blank=True) 
    expire_time = models.DateTimeField(verbose_name=_("زمان ابطال"), null = True , blank= True)
    is_confirmed = models.BooleanField(default=False)
    objects = UserManager()

    def __str__(self):
        if self.fullname:
            return self.fullname
        else:
            return self.username

    class Meta:
        ordering = ['username']
        verbose_name = _('کاربر')
        verbose_name_plural = _('کاربران')

class Patogh(models.Model):
    id = models.UUIDField(verbose_name=_("شناسه"),primary_key=True, default=uuid.uuid4,help_text="Unique Id for this Patogh")
    creator_id = models.ForeignKey(User , verbose_name=_("شناسه پدید آورنده"),on_delete= models.CASCADE)
    name = models.CharField(verbose_name=_("نام"),max_length=100)
    state = (
        ('1','public'),
        ('2','private')
    )
    status = models.CharField(verbose_name=_("حالت دورهمی"),choices=state , max_length=10 )
    telephone = models.CharField(verbose_name=_("شماره تلفن"),max_length=12)
    is_telephone_verified = models.CharField(verbose_name=_("صحت شماره تلفن"),choices= verify_state,max_length=10,default='-1')
    address = models.CharField(verbose_name=_("آدرس"),max_length=1000)
    longitude = models.FloatField(verbose_name=_("عرض جغرافیایی"),null=True,blank=True)
    latitude = models.FloatField(verbose_name=_("طول جغرافیایی"),null=True,blank=True)
    city = models.ForeignKey(City , verbose_name=_("شهر"),on_delete=models.PROTECT , null = True,blank=True)
    location_type = models.ForeignKey(LocationTypes ,verbose_name=_("مکان"), on_delete=PROTECT , null=True, blank=True)
    description = models.CharField(verbose_name=_("توضیحات"),max_length=1000,null = True , blank = True)
    profile_image_url = models.ImageField(verbose_name=_("عکس پروفایل"),
                                           upload_to = patogh_image_directory_path ,
                                           null = True , blank = True, help_text = _("JPG, JPEG or PNG is validate"),
                                           validators =[FileExtensionValidator(VALID_IMAGE_FORMAT),validate_image_size])
    tags_id = models.ForeignKey(Tags ,verbose_name=_("شناسه برچست"), on_delete=models.CASCADE ,null=True,blank=True)
    category = models.ForeignKey(PatoghCategory, on_delete= models.CASCADE , verbose_name=_("کتگوری"), null=True, blank = True )
    wifi = models.BooleanField(default=False,verbose_name=_("وای فای"), null=True, blank = True)
    poz = models.BooleanField(default=False,verbose_name=_("دستگاه پوز"), null=True, blank = True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        unique_together = ('id','creator_id')
        verbose_name = _('پاتوق')
        verbose_name_plural = _('پاتوق ها')

class PendingVerify(models.Model):
    receptor = models.OneToOneField(User,verbose_name=_("دریافت کننده"),primary_key=True, max_length=50,on_delete=CASCADE)
    otp = models.IntegerField(verbose_name=_("OTP کد"))
    send_time = models.DateTimeField(verbose_name=_("زمان ارسال"),null = True)
    allowed_try = models.SmallIntegerField(verbose_name=_(" دفعات مجاز برای تلاش"),default=5
                                           ,validators =[MinValueValidator(0),MaxValueValidator(5)])

    def __str__(self):
        return self.receptor

    class Meta:
        ordering = ['send_time']
        verbose_name = _('تاییدیه')
        verbose_name_plural = _('تاییدیه ها')


class UsersPermision(models.Model):
    id = models.UUIDField(verbose_name=_("شناسه"),primary_key=True, default=uuid.uuid4,help_text="Unique Id for this User Permision")
    label = models.CharField(verbose_name=_("برچسب"),unique = True ,max_length=30,null=True)

    class Meta:
        ordering = ['id']
        verbose_name = _('تایید کاربر')
        verbose_name_plural = _('تایید کاربران')

class GatheringHaveMember(models.Model):
    id = models.UUIDField(primary_key=True, verbose_name=_("شناسه"),default=uuid.uuid4,help_text="Unique Id for this gathering")
    g_id = models.ForeignKey(Patogh ,verbose_name=_("شناسه پاتوق"), on_delete= models.CASCADE)
    username = models.ForeignKey(User , verbose_name=_("نام کاربری"),on_delete=models.CASCADE, max_length=30)
    permission=(
        (0,'normal member'),
        (1,'deleted'),
        (2,'quit')
    )
    status = models.SmallIntegerField(verbose_name=_("حالت پذیرش کاربر"),default=0, choices=permission)
    class Meta:
        ordering = ['username']
        unique_together = ('g_id','username')
        verbose_name = _('عضو دورهمی')
        verbose_name_plural = _('اعضای دورهمی')

    def __str__(self):
        return self.username.username 


class Gathering(models.Model):
    id = models.UUIDField(primary_key=True, verbose_name=_("شناسه"),default=uuid.uuid4,help_text="Unique Id for this gathering")
    creator_id = models.ForeignKey(User,verbose_name=_("شناسه پدید آورنده"), on_delete=models.PROTECT , null= True )
    patogh_id = models.ForeignKey(Patogh , verbose_name=_("شناسه پاتوق"),on_delete=models.PROTECT , null = True)
    name = models.CharField(verbose_name=_("نام"),max_length=50 , null = True , blank=True)
    state = (
        ('0', 'uncommited'),
        ('1', 'commited')
    )
    status = models.SmallIntegerField(verbose_name=_("حالت دورهمی"),default=0, choices=state)
    city = models.ForeignKey(City, verbose_name=_("شهر"), on_delete=models.PROTECT, null=True, blank=True)
    start_time = models.DateTimeField(verbose_name=_("زمان شروع"),help_text="Start time for the patogh",null = True)
    end_time = models.DateTimeField(verbose_name=_("زمان پایان"),help_text="end time for the patogh",null = True)
    description = models.CharField(verbose_name=_("توضیحات"),help_text="descripe your patogh", max_length=1000)
    gender = (
        ('0', 'Female Only'),
        ('1','Male Only'),
        ('-1','No filter')
    )
    gender_filter = models.SmallIntegerField(verbose_name=_("جنسیت"),default= -1 , choices= gender)
    members_count = models.IntegerField(verbose_name=_("تعداد اعضا"),default= -1 , help_text="-1 means no filter")
    min_age = models.IntegerField(verbose_name=_("کمترین سن"),default= -1 , help_text="-1 means no filter")
    max_age = models.IntegerField(verbose_name=_("بالاترین سن"),default= -1 , help_text="-1 means no filter")
    tags_id = models.ForeignKey(Tags ,verbose_name=_("شناسه برچسب"),on_delete=models.PROTECT , null = True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = _('دورهمی')
        verbose_name_plural = _('دورهمی ها')

class JoinGatheringRequest(models.Model):
    g_id = models.ForeignKey(Gathering , verbose_name=_("شناسه دورهمی"),on_delete= models.CASCADE)
    username = models.ForeignKey(User , verbose_name=_("نام کاربری"),on_delete= models.CASCADE)
    state = (
        ('0','requested'),
        ('1','accepted'),
        ('2','rejected')
    )
    status = models.SmallIntegerField(verbose_name=_("وضعیت درخواست"),choices=state)

    def __str__(self):
        return self.username + " state request is "+ self.status

    class Meta:
        ordering = ['g_id']
        unique_together = ('g_id','username')
        verbose_name = _('درخواست پیوستن')
        verbose_name_plural = _('درخواست های پیوستن')

class PatoghsComments(models.Model):
    id = models.UUIDField(verbose_name=_("شناسه"),primary_key=True, default=uuid.uuid4,help_text="Unique Id for this patogh Commments")
    sender = models.ForeignKey(User, verbose_name=_("فرستنده"),on_delete=models.PROTECT, null = True)
    patogh_id = models.ForeignKey(Patogh , verbose_name=_("شناسه پاتوق"),on_delete=models.PROTECT, null = True)
    reply_to = models.ForeignKey('self' ,verbose_name=_("بازخورد به"), on_delete=models.CASCADE )
    send_time = models.DateTimeField(verbose_name=_("زمان ارسال"),auto_now_add=True, blank= True)
    comment = models.CharField(verbose_name=_("نظر"),max_length=1000)

    def __str__(self):
        return self.id + " has commented " + self.comment

    class Meta:
        ordering = ['id']
        verbose_name = _('نظر در مورد پاتوق')
        verbose_name_plural = _('نظرات در مورد پاتوق')

class reportedPatogh(models.Model):
    patogh_id = models.ForeignKey(Patogh  ,verbose_name=_("شناسه پاتوق"), on_delete= models.PROTECT)
    username = models.ForeignKey(User ,verbose_name=_("نام کاربری"), on_delete= models.PROTECT )
    massage = models.CharField(verbose_name=_("پیام"),max_length=1000)
    send_time = models.DateTimeField(verbose_name=_("زمان ارسال"),auto_now_add=True, blank= True)

    def __str__(self):
        return self.patogh_id
    class Meta:
        ordering = ['patogh_id']
        unique_together = ('patogh_id','username')
        verbose_name = _('پاتوق گزارش شده')
        verbose_name_plural = _('پاتوق های گزارش شده')

class PatoghHaveImages(models.Model):
    patogh_id = models.ForeignKey(Patogh ,verbose_name=_("شناسه پاتوق"), on_delete= models.CASCADE)
    image_url = models.ImageField(verbose_name=_("عکس برای دورهمی"),
                                  upload_to = dorhami_image_profile_directory_path ,
                                  null = True , blank = True, help_text = _("JPG, JPEG or PNG is validate"),
                                  validators =[FileExtensionValidator(VALID_IMAGE_FORMAT),validate_image_size])
    state = (
        ('0','registered'),
        ('1','accepted'),
        ('2','rejected'),
        ('3','deleted')
    )
    status = models.SmallIntegerField(verbose_name=_("وضعیت تایید عکس"),choices= state, default= 0)
    send_time = models.DateTimeField(verbose_name=_("زمان ارسال"),auto_now_add=True , null = True , blank= True)

    def __str__(self):
        return self.patogh_id + " has " +self.state

    class Meta:
        ordering = ['patogh_id']
        verbose_name = _('عکس پاتوق')
        verbose_name_plural = _('عکس های پاتوق')


class UsersHavePermisions(models.Model):
    username = models.ForeignKey(User ,verbose_name=_("نام کاربری"), on_delete= models.CASCADE)
    permision_id = models.ForeignKey(UsersPermision , verbose_name=_("شناسه تاییدیه"),on_delete= models.CASCADE)

    def __str__(self):
        return self.username + " have permission id: " + self.permision_id
    class Meta:
        ordering = ['username']
        unique_together = ('username','permision_id')
        verbose_name = _('وضعیت درخواست')
        verbose_name_plural = _('وضعیت درخواست ها')



class GatheringScheduall(models.Model):
    g_id = models.ForeignKey(Gathering,verbose_name=_("شناسه دورهمی"), on_delete=models.CASCADE )
    status = (
        ('0','active with out repeat'),
        ('1','repeat'),
        ('2','unactive')
    )
    Sa = models.SmallIntegerField(verbose_name=_("شنبه"),choices=status)
    Su = models.SmallIntegerField(verbose_name=_("یک شنبه"),choices=status)
    Mo = models.SmallIntegerField(verbose_name=_("دو شنبه"),choices=status)
    Tu = models.SmallIntegerField(verbose_name=_("سه شنبه"),choices=status)
    We = models.SmallIntegerField(verbose_name=_("چهار شنبه"),choices=status)
    Th = models.SmallIntegerField(verbose_name=_("پنج شنبه"),choices=status)
    Fr = models.SmallIntegerField(verbose_name=_("جمعه"),choices=status)

    def __str__(self):
        return self.g_id
    class Meta: 
        ordering = ['g_id']
        verbose_name = _('برنامه زمانی')
        verbose_name_plural = _('برنامه های زمانی')

