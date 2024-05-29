from django.db import models

from django.contrib.auth.models import User #user,pwd,f_n,l_n,ema..pro

# Create your models here.
class Profile(models.Model):
    GENDER = (
        ('M','Male'),
        ('F','Female'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=50, unique=True)
    fullname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    gender = models.CharField(max_length=50,choices=GENDER)
    profile_pix = models.ImageField(upload_to='profile', null=True,blank=True)

    def __str__(self):
        return self.username

