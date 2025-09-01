# irctc_clone/models.py

from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
# User Profile 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.user.username

# Automatically create profile for each user
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)


# Train model
class Train(models.Model):
    train_no = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    source = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    seats = models.IntegerField()
    fare = models.IntegerField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()

    def __str__(self):
        return self.name


# Booking model
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pnr = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    email = models.EmailField(null=True, blank=True)  # <-- Fixed here
    from_station = models.CharField(max_length=100,null=True,blank=True)
    to_station = models.CharField(max_length=100,null=True,blank=True)
    journey_date = models.DateField(null=True,blank=True)
    seats = models.PositiveIntegerField(null=True,blank=True)
    booked_at = models.DateTimeField(auto_now_add=True,null=True)  # only default, not auto_now_add

    def __str__(self):
        return f"PNR: {self.pnr} - {self.name}"
