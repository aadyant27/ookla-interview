from django.db import models
from django.utils import timezone


# Create your models here.
class Event(models.Model):
    event_name = models.CharField(max_length=200, unique=True)
    date_of_event = models.DateTimeField()
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_tickets = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField() # Reserve tickets in advance

    def __str__(self):
        return self.event_name
    
class Booking(models.Model):
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15)
    event_name = models.CharField(max_length=200)
    ticket_price_paid = models.DecimalField(max_digits=10, decimal_places=2)
    tickets_purchased = models.PositiveIntegerField()
    date_time = models.DateTimeField(default=timezone.now)
    surge_price_paid = models.BooleanField(default=False) # For Data-analysis
 
    def __str__(self):
        return f'{self.email} booking for {self.event_name}'