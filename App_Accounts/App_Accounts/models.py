from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver

GENDER_CHOICE=(
    ('male','Male'),
    ('female','Female'),
)
SELECT_BLOOD_GROUP=(
    ('A+','A+'),
    ('B+','B+'),
    ('O+','O+'),
    ('AB+','AB+'),
    ('A-','A-'),
    ('B-','B-'),
    ('O-','O-'),
    ('AB-','AB-'),
)
USER_TYPE=(
    ('blood doner','Blood Doner'),
)

RELIGION_CHOICE=(
    ('muslim','Muslim'),
    ('hinduism','Hinduism'),
    ('buddhism','Buddhism'),
    ('christianity','Christianity'),
)
class BloodGroup(models.Model):
    name=models.CharField(max_length=20)

    def __str__(self):
        return self.name

class HLogin(models.Model):
    username=models.CharField(max_length=30)
    password=models.CharField(max_length=30)

    def __str__(self):
        return self.username

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    type=models.CharField(choices=USER_TYPE,max_length=20,blank=True)
    phone=models.CharField(blank=True,max_length=11)
    city=models.CharField(blank=True,max_length=20)
    address=models.CharField(blank=True,max_length=100)
    facebook=models.CharField(blank=True,max_length=100)
    twitter=models.CharField(blank=True,max_length=100)
    instragam=models.CharField(blank=True,max_length=100)
    linkedin=models.CharField(blank=True,max_length=100)
    gender=models.CharField(choices=GENDER_CHOICE,blank=True,max_length=30)
    bloodgroup=models.CharField(choices=SELECT_BLOOD_GROUP,blank=True,null=True,max_length=20)
    religion=models.CharField(blank=True,max_length=20,choices=RELIGION_CHOICE)
    totaldonate=models.IntegerField(default=0)
    image=models.ImageField(upload_to="Profile/",default="avatar7.png")
    dob=models.DateField(blank=True,null=True)
    lastdonate=models.DateField(blank=True,null=True)
    aboutyou=models.TextField(blank=True)
    points=models.IntegerField(blank=True,null=True)
    totalDonationCount=models.IntegerField(blank=True,null=True)
    latestHospital = models.CharField(blank=True,max_length=500)
    latestCity = models.CharField(blank=True,max_length=500)
    latestName = models.CharField(blank=True,max_length=500)


    def __str__(self):
        return '{}'.format(self.user)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class user_Apportionment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name=models.CharField(max_length=120)
    gender=models.CharField(max_length=120)
    date_of_birth=models.CharField(max_length=120)
    mobile_no=models.CharField(max_length=120)
    address=models.CharField(max_length=120)
    apportionment_date=models.DateField(max_length=120)
    state=models.CharField(max_length=120)
    city=models.CharField(max_length=120)
    blood_bank_name=models.CharField(max_length=120)
    blood_group=models.CharField(max_length=120)
    g_id=models.CharField(max_length=120)

    def __str__(self):
        return '{}-{}'.format(self.user,self.blood_bank_name)