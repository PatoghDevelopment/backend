from _typeshed import OpenBinaryModeReading
from typing import Sized
from django.db import models
import uuid
from datetime import date
import hashlib
from django.db.models import indexes 
from django.db.models.base import Model
from django.db.models.fields import CharField

class City(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text="Unique Id for this City")
    city_status = (
        ('Tehran'),
        ('Qom'),
        ('Sistan'),
        ('Khozestan'),
        ('Gorgan'),
        ('Golestan'),
        ('Alborz'),
        ('Kerman'),
        ('Ardebil'),
        ('Markazi'),
        ('Khorasan razavi'),
        ('Khorasan shomali'),
        ('Khorasan jonobi'),
        ('Boshehr'),
        ('Esfahan'),
        ('Hamedan'),
        ('Kermanshah'),
        ('Azarbaijan gharbi'),
        ('Azarbaijan sharhgi'),
        ('Fars'),
        ('Yazd'),
        ('Hormozgan'),
        ('Semnan'),
        ('Qazvin')
    )
    name = models.CharField(max_length=40,choices=city_status,help_text="Where do you live?",null = True , blank = True)
    
    class Meta:
        ordering = ['name']
   
class Users(models.Model):
    username = models.CharField(primary_key=True,max_length=100,unique=True)
    fullname = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=12,null=True,blank=True)
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

class Patogh(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text="Unique Id for this Patogh")
    creator_id = models.CharField(primary_key=True, max_length=50)
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
    location_type = models.SmallIntegerField()
    description = models.CharField(max_length=1000,null = True , blank = True)
    profile_image_url = models.CharField(max_length=128 , null=True,blank=True)
    tags_id = models.ForeignKey()#add      tag ---------------
    class Meta:
        ordering = ['name']

class PendingVerify(models.Model):
    receptor = models.CharField(primary_key=True, max_length=50)
    otp = models.IntegerField()
    send_time = models.DateTimeField(null = True)
    allowed_try = models.SmallIntegerField(default=5)

    class Meta:
        ordering = ['send_time']

class UsersHavePermisions(models.Model):
    username = models.CharField(primary_key=True)
    permision_id = models.IntegerField(null = True)

    class Meta:
        ordering = ['username']

class UsersPermision(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text="Unique Id for this User Permision")
    title = models.CharField(max_length=30,null=True)

    class Meta:
        ordering = ['title']