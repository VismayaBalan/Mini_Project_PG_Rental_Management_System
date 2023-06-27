from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Pglist(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    address = models.TextField()
    phoneNumber = models.IntegerField()
    image = models.ImageField(upload_to='login/pglist_images')

    def __str__(self):
        return self.name


    
class User(AbstractUser):
    role = models.CharField(max_length=10)

    def __str__(self):
        return str(self.username)
    
class Customer(models.Model):
    uuser = models.OneToOneField(User,on_delete = models.CASCADE,related_name='customer')
    plocation = models.CharField(max_length=30)
    description = models.CharField(max_length=100)