from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    
    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=200)
    asset = models.ImageField(upload_to="event_images/", default="event_images/default.jpg")
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    participants = models.ManyToManyField(User, related_name='rsvp_events', blank=True)
    
    def __str__(self):
        return f"{self.name}"

