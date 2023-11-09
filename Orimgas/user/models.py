from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from orimgasapp.models import Company

class User(AbstractUser):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    date_of_birth = models.DateField(null=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    company = models.ForeignKey(Company, verbose_name='company',
                                on_delete=models.CASCADE, 
                                related_name='users', null=True, blank=True)
