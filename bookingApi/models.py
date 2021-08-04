from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class UserProfile(models.Model):  
    user = models.OneToOneField(User, related_name='profile',on_delete=models.CASCADE)
    location = models.CharField(max_length=140)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    address = models.TextField()
    
    class Meta:
        default_permissions = ()

    def __str__(self):
        return 'Profile of user: {}'.format(self.user.username)
    
class Vehicle(models.Model):
    TYPE = (
        (1, 'bike'),
        (2, 'car')
    )
    vehicleOwner=models.ForeignKey(UserProfile,on_delete=models.CASCADE, related_name='owner')
    vehicleName= models.CharField(max_length=50,blank=True)
    vehicleRegNumber= models.CharField(max_length=50,unique=True)
    vehicleType =  models.IntegerField(choices=TYPE)
    vehicleSpec=models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    availability=models.BooleanField()
    bookingUpto = models.DateTimeField()
    
    class Meta:
            default_permissions = ()

    def __str__(self):
        return (self.vehicleRegNumber)
    
    
class BookingPrice(models.Model):
    vehicle = models.ManyToManyField(Vehicle,related_name='vehicle')
    price= models.DecimalField(max_digits=8, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
            default_permissions = ()

    def __str__(self):
        return str(self.price)
    
class bookingDate(models.Model):
    customer=models.ForeignKey(UserProfile,on_delete=models.CASCADE, related_name='customer')
    vehicle=models.ForeignKey(Vehicle,on_delete=models.CASCADE, related_name='vehicle_name')
    datetimeFrom = models.DateTimeField()
    datetimeTo = models.DateTimeField()
    bookingStatus=models.BooleanField()
    booked_datetime = models.DateTimeField(auto_now_add=True)
    
    class Meta:
            default_permissions = ()

    def __str__(self):
        return (self.customer.user.username)
    
    
