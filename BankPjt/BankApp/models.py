from django.db import models

# Create your models here.
class Register(models.Model):
    accno=models.IntegerField()
    name=models.CharField(max_length=50)
    addr=models.CharField(max_length=50)
    bal=models.IntegerField()
    uname=models.CharField(max_length=50)
    pwd=models.CharField(max_length=50)

