from django.db import models
from datetime import date
from datetime import datetime

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
