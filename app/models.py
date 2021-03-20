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
