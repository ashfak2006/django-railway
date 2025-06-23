from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="customer_profile")
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True,blank=True)
    male='M'
    female='F'
    gender_choices=((male,"MALE"),(female,"FEMALE"))
    gender = models.CharField(choices=gender_choices,default='M',null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    LIVE=1
    DELETE=0
    DELETE_CHOICES=((DELETE,"DELETE"),(LIVE,"LIVE"))
    DELETE_STATUS=models.IntegerField(choices=DELETE_CHOICES,default=1)


    def __str__(self):
        return self.user.username
    

class Adress(models.Model):
    TYPES=(
        ('shipping','shipping'),
        ('biling','billling')
    )
    type=models.CharField(choices=TYPES,default='shipping')
    Adresstype=(
        ('Home','Home'),
        ('Work','Work')
    )
    adress_type=models.CharField(choices=Adresstype,default='Home')
    phonenumber=models.CharField(max_length=20,null=True,blank=True)
    pincode=models.IntegerField()
    state=models.CharField(max_length=50,null=True,blank=True)
    house_no=models.CharField(max_length=50,null=True,blank=True)
    city=models.CharField(max_length=50,null=True,blank=True)
    road_name=models.CharField(max_length=50,null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    landmark=models.TextField(null=True,blank=True)
    owner=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='adress',null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)