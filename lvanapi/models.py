from django.db import models

class UserInfo(models.Model):
    username=models.CharField(max_length=16)
    password=models.CharField(max_length=32)

# Create your models here.
class HostInfo(models.Model):
    hostname=models.CharField(max_length=32)
    inner_ip=models.CharField(max_length=16)
    outer_ip=models.CharField(max_length=32)
    cpu=models.CharField(max_length=2)
    memory=models.CharField(max_length=3)
    disk_size=models.CharField(max_length=3)
    
