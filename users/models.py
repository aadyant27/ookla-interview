# Create your models here.
from django.db import models

# Create your models here.
    
class User(models.Model):
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.email