from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
# Create your models here.



class Service(models.Model):
    title = models.CharField(max_length=100)
    information = models.TextField()
    contact = models.CharField(max_length=20)
    cost = models.CharField(max_length=20)
    image = models.ImageField(default='default.jpg',upload_to='images/')
    
    def __str__(self):
       return self.title



class RequestService(models.Model):
    fname = models.CharField(max_length=42)
    lname = models.CharField(max_length=42)
    email = models.EmailField(max_length=75)
    contactnumber = models.CharField(max_length=20)
    purpose = models.TextField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)



class OpenJob(models.Model):
    jobname = models.CharField(max_length=42)
    payrange = models.CharField(max_length=75)
    jobtype = models.CharField(max_length=42)
    location = models.CharField(max_length=75)

    def __str__(self):
       return self.jobname



class BranchLocation(models.Model):
    branchname = models.CharField(max_length=75)
    building = models.CharField(max_length=75)
    street = models.CharField(max_length=75)
    city = models.CharField(max_length=75)
    state = models.CharField(max_length=75)    
    email = models.EmailField(max_length=75)
    contactnumber = models.CharField(max_length=20)

    def __str__(self):
       return self.branchname




class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=75)
    lname = models.CharField(max_length=75)
    email = models.EmailField(max_length=75)
    gender = models.CharField(max_length=75)
    dateofbirth = models.DateField()
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=75)
    state = models.CharField(max_length=75)
    pincode = models.IntegerField()
    contactnumber = models.CharField(max_length=20)
    expectedsalary = models.CharField(max_length=75)
    education = models.CharField(max_length=75)
    workexperience = models.CharField(max_length=75)
    status = models.CharField(max_length=75,default='Pending')    
    jobpost = models.ForeignKey(OpenJob,on_delete=models.CASCADE)



class Course(models.Model):
    name = models.CharField(max_length=75)
    cost = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    course = models.ManyToManyField(Course,blank=True)

    def __str__(self):
        return self.user.username
 



@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class OrderItem(models.Model):
    course = models.OneToOneField(Course,on_delete=models.CASCADE,null=True)
    is_ordered = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now=True)
    date_ordered = models.DateTimeField(null=True)


    def __str__(self):
        return self.course.name





class Order(models.Model):
    ref_code = models.CharField(max_length=15)
    owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    is_ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    date_ordered = models.DateTimeField(auto_now=True)
    

    

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.course.cost for item in self.items.all()])

    def __str__(self):
        return '{0} - {1}'.format(self.owner, self.ref_code)        
  
  
class DeliveryAdd(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=75)
    state = models.CharField(max_length=75)
    pincode = models.IntegerField()

    def __str__(self):
        return self.user.username
 
