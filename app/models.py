from django.db import models
from datetime import date
from datetime import datetime
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from django.urls import reverse

# Create your models here.
class News(models.Model):
    topic = models.CharField(max_length=200,unique=True)
    description = models.CharField(max_length=200)
    date = models.DateField(default=datetime.now)
    image = models.ImageField(upload_to='news',null=True, blank=True)

    def __str__(self):
        return self.topic

class Workers(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Servicetypes(models.Model):
    type = models.CharField(max_length=200)

    def __str__(self):
        return self.type

class Services(models.Model):
    name = models.CharField(max_length=200,unique=True)
    service_type = models.ForeignKey(Servicetypes,on_delete=models.CASCADE)
    person = models.ForeignKey(Workers, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return self.name

class UserProfileInfo(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    GENDER_CHOICES = (
        ('M', 'Mężczyzna'),
        ('K', 'Kobieta'),
        )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=9,validators=[RegexValidator(r'^\d{1,10}$')])
    birth_date = models.DateField()

    # this makes my User Model fields required in registration panel
    User._meta.get_field('email').blank = False
    User._meta.get_field('first_name').blank = False
    User._meta.get_field('last_name').blank = False

    def __str__(self):
        return self.user.get_full_name()

class Event(models.Model):
    title = models.ForeignKey(Services,on_delete=models.CASCADE)
    doctor = models.ForeignKey(Workers,on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    def __str__(self):
      return self.title
