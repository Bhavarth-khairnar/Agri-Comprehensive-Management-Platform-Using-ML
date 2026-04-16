from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Crop_Details(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    farmer_id = models.BigAutoField(primary_key=True)

    farmer_name = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)

    n = models.PositiveIntegerField()
    p = models.PositiveIntegerField()
    k = models.PositiveIntegerField()

    temperature = models.FloatField()
    humidity = models.FloatField()
    ph = models.FloatField()
    rainfall = models.FloatField()

    soil_type = models.CharField(max_length=20, null=True, blank=True)
    season = models.CharField(max_length=20, null=True, blank=True)
    region = models.CharField(max_length=20, null=True, blank=True)

    prediction = models.CharField(max_length=50)
    fertilizer = models.CharField(max_length=50)

    date = models.DateField()

    def __str__(self):
        return self.farmer_name
    
class fert_Details(models.Model):
    farmer_name = models.CharField(max_length=100)
    n = models.PositiveIntegerField()
    p = models.PositiveIntegerField()
    k = models.PositiveIntegerField()
    temperature = models.CharField(max_length=20)
    humidity = models.CharField(max_length=20)
    prediction = models.CharField(max_length=50)
    fertilizer = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.farmer_name
    
class images_data(models.Model):
      Images = models.FileField(upload_to='Images')    

class image_data(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    Images = models.FileField(upload_to='crop_images/')
    quantity = models.PositiveIntegerField()
    
    def __str__(self):
        return f"{self.Images.name} - {self.quantity} Kg"

class Vendor(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email