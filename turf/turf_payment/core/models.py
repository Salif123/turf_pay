from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime

class Stadium(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveBigIntegerField(null=True)
    location = models.CharField(max_length=255)
    booked = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_slot = models.DateTimeField()
    phone = models.CharField(max_length=15)
    stadium = models.ForeignKey(Stadium, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.time_slot} at {self.stadium.name}"