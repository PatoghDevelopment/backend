from django.db import models
import uuid
from datetime import date
import hashlib
from django.db.models import indexes 
from django.db.models.base import Model
from django.db.models.deletion import PROTECT
from django.db.models.fields import CharField
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


class LocationTypes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text="Unique Id for this Location")
    label = models.CharField(max_length=20 , unique=True)

    class Meta:
        ordering = ['id']


class Tags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text="Unique Id for this Tag")
    tag = models.CharField(unique=True,max_length=40)

    class Meta:
        ordering = ['id']
        unique_together = ('id','tag')

class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text="Unique Id for this City")
    city_status = (
        ('0','Tehran'),
        ('1','Qom'),
        ('2','Sistan'),
        ('3','Khozestan'),
        ('4','Gorgan'),
        ('5','Golestan'),
        ('6','Alborz'),
        ('7','Kerman'),
        ('8','Ardebil'),
        ('9','Markazi'),
        ('10','Khorasan razavi'),
        ('11','Khorasan shomali'),
        ('12','Khorasan jonobi'),
        ('13','Boshehr'),
        ('14','Esfahan'),
        ('15','Hamedan'),
        ('16','Kermanshah'),
        ('17','Azarbaijan gharbi'),
        ('18','Azarbaijan sharhgi'),
        ('19','Fars'),
        ('20','Yazd'),
        ('21','Hormozgan'),
        ('22','Semnan'),
        ('23','Qazvin')
    )
    name = models.CharField(max_length=40,choices=city_status,help_text="Where do you live?")
    
    class Meta:
        ordering = ['name']
        unique_together = ('id','name')
   
class Users(models.Model):
    username = models.CharField(primary_key=True,max_length=100,unique=True)
    fullname = models.CharField(max_length=100)
    email = models.CharField(unique=True, max_length=50)
    phone = models.CharField(unique = True, max_length=12,null=True,blank=True)
    password = hashlib.sha256('Password'.encode("UTF-8")) 
    birthdate = models.DateField()
    city = models.ForeignKey(City , on_delete=models.PROTECT , null = True)
    gender_status = (
        ('0','female'),
        ('1','male')
    )
    gender = models.CharField(max_length=6,choices=gender_status,blank=True)
    profile_image_url = models.CharField(max_length=128,null = True , blank = True)
    bio = models.CharField(max_length=1000,null = True , blank = True)
    last_login_try = models.TimeField('last login',null = True , blank = True) 
    
    def __str__(self):
        return self.fullname

    class Meta:
        ordering = ['username']

class Patogh(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text="Unique Id for this Patogh")
    creator_id = models.ForeignKey(Users , on_delete= models.CASCADE)
    name = models.CharField(max_length=100)
    state = (
        ('1','public'),
        ('2','private')
    )
    status = models.CharField(choices=state , max_length=10 )
    telephone = models.CharField(max_length=12)
    verify_state = (
        ('0','registered'),
        ('1','verified')
    )
    is_telephone_verified = models.CharField(choices= verify_state,max_length=10)
    address = models.CharField(max_length=1000)
    longitude = models.FloatField()
    latitude = models.FloatField()
    city = models.ForeignKey(City , on_delete=models.PROTECT , null = True)
    location_type = models.ForeignKey(LocationTypes , on_delete=PROTECT , null=True, blank=True)
    description = models.CharField(max_length=1000,null = True , blank = True)
    profile_image_url = models.CharField(max_length=128 , null=True,blank=True)
    tags_id = models.ForeignKey(Tags , on_delete=models.CASCADE )
    class Meta:
        ordering = ['name']
        unique_together = ('id','creator_id')

class PendingVerify(models.Model):
    receptor = models.CharField(primary_key=True, max_length=50)
    otp = models.IntegerField()
    send_time = models.DateTimeField(null = True)
    allowed_try = models.SmallIntegerField(default=5)

    class Meta:
        ordering = ['send_time']


class UsersPermision(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text="Unique Id for this User Permision")
    label = models.CharField(unique = True ,max_length=30,null=True)

    class Meta:
        ordering = ['id']

class GatheringHaveMember(models.Model):
    g_id = models.ForeignKey(Patogh , on_delete= models.CASCADE)
    username = models.ForeignKey(Users , on_delete=models.CASCADE, max_length=30)
    permission=(
        ('0','normal member'),
        ('1','deleted'),
        ('2','quit')
    )
    status = models.SmallIntegerField(default=0, choices=permission)
    class Meta:
        ordering = ['username']
        unique_together = ('g_id','username')

class Gathering(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text="Unique Id for this gathering")
    creator_id = models.ForeignKey(Users, on_delete=models.PROTECT , null= True )
    patogh_id = models.ForeignKey(Patogh , on_delete=models.PROTECT , null = True)
    name = models.CharField(max_length=50 , null = True , blank=True)
    state = (
        ('0', 'uncommited'),
        ('1', 'commited')
    )
    status = models.SmallIntegerField(default=0, choices=state)
    start_time = models.DateTimeField(help_text="Start time for the patogh",null = True)
    end_time = models.DateTimeField(help_text="end time for the patogh",null = True)
    description = models.CharField(help_text="descripe your patogh", max_length=1000)
    gender = (
        ('0', 'Female Only'),
        ('1','Male Only'),
        ('-1','No filter')
    )
    gender_filter = models.SmallIntegerField(default= -1 , choices= gender)
    members_count = models.IntegerField(default= -1 , help_text="-1 means no filter")
    min_age = models.IntegerField(default= -1 , help_text="-1 means no filter")
    max_age = models.IntegerField(default= -1 , help_text="-1 means no filter")
    tags_id = models.ForeignKey(Tags ,on_delete=models.PROTECT , null = True)

    class Meta:
        ordering = ['id']

class JoinGatheringRequest(models.Model):
    g_id = models.ForeignKey(Gathering , on_delete= models.CASCADE)
    username = models.ForeignKey(Users , on_delete= models.CASCADE)
    state = (
        ('0','requested'),
        ('1','accepted'),
        ('2','rejected')
    )
    status = models.SmallIntegerField(choices=state)

    class Meta:
        ordering = ['g_id']
        unique_together = ('g_id','username')

class PatoghsComments(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text="Unique Id for this patogh Commments")
    sender = models.ForeignKey(Users, on_delete=models.PROTECT, null = True)
    patogh_id = models.ForeignKey(Patogh , on_delete=models.PROTECT, null = True)
    reply_to = models.ForeignKey('self' , on_delete=models.CASCADE )
    send_time = models.DateTimeField(auto_now_add=True, blank= True)
    comment = models.CharField(max_length=1000)

    class Meta:
        ordering = ['id']

class reportedPatogh(models.Model):
    patogh_id = models.ForeignKey(Patogh  , on_delete= models.PROTECT)
    username = models.ForeignKey(Users , on_delete= models.PROTECT )
    massage = models.CharField(max_length=1000)
    send_time = models.DateTimeField(auto_now_add=True, blank= True)

    def __str__(self):
        return self.patogh_id
    class Meta:
        ordering = ['patogh_id']
        unique_together = ('patogh_id','username')

class PatoghHaveImages(models.Model):
    patogh_id = models.ForeignKey(Patogh , on_delete= models.CASCADE)
    image_url = models.CharField(max_length=128)
    state = (
        ('0','registered'),
        ('1','accepted'),
        ('2','rejected'),
        ('3','deleted')
    )
    status = models.SmallIntegerField(choices= state, default= 0)
    send_time = models.DateTimeField(auto_now_add=True , null = True , blank= True)

    class Meta:
        ordering = ['patogh_id']


class UsersHavePermisions(models.Model):
    username = models.ForeignKey(Users , on_delete= models.CASCADE)
    permision_id = models.ForeignKey(UsersPermision , on_delete= models.CASCADE)

    class Meta:
        ordering = ['username']
        unique_together = ('username','permision_id')



class GatheringScheduall(models.Model):
    g_id = models.ForeignKey(Gathering, on_delete=models.CASCADE )
    status = (
        ('0','default'),
        ('1','repeat')
    )
    Sa = models.SmallIntegerField(choices=status)
    Su = models.SmallIntegerField(choices=status)
    Mo = models.SmallIntegerField(choices=status)
    Tu = models.SmallIntegerField(choices=status)
    We = models.SmallIntegerField(choices=status)
    Th = models.SmallIntegerField(choices=status)
    Fr = models.SmallIntegerField(choices=status)

    class Meta: 
        ordering = ['g_id']
