from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User 
from django.http import request, HttpResponse

class Company(models.Model):
    name = models.CharField(max_length=50)
    company_code = models.CharField(max_length=50)
    exec = models.CharField(max_length=50) 

    def __str__(self):
        return f'{self.name}, company code: {self.company_code}'

class Position(models.Model): 
    name = models.CharField(max_length=50)
    company = models.ForeignKey(Company,verbose_name=_('company'), on_delete=models.CASCADE, related_name='company_position')

    def __str__(self):
        return f'{self.name}'

class Instruction(models.Model):
    name = models.CharField(max_length=50)
    company = models.ForeignKey(Company,verbose_name=_('company'), on_delete=models.CASCADE, related_name='company_instruction')
    position = models.ForeignKey(Position,verbose_name=_('position'), on_delete=models.CASCADE, related_name='position_instruction') 
    pdf = models.FileField(upload_to='instructions')

    def __str__(self):
        return f'{self.name}'
    
class Supervisor(AbstractUser):
    pass


class RegularUser(AbstractUser):
    pass


class User(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    company = models.ForeignKey(Company,verbose_name=_('company'), on_delete=models.CASCADE, related_name='company_user')
    birthdate = models.DateField()
    position = models.ForeignKey(Position,verbose_name=_('position'), on_delete=models.CASCADE, related_name='user_position')
    email = models.EmailField(_("email address"), max_length=254)
    phone_number = PhoneNumberField(_("phone number"), max_length=15, blank=True) 
    supervisor = models.BooleanField(default=False)
    regular_user = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name} {self.surname}'
    
    def create_regular_user(request, company_id):
        if request.self.supervisor:
            # Check if the requesting user is a supervisor

            # Extract data for the new regular user
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            email = request.POST.get('email')
            birthdate = request.POST.get('birthdate')
            # Other required fields

            # Create a new RegularUser associated with the company
            regular_user = User.objects.create(
                name=name,
                surname=surname,
                email=email,
                birthdate=birthdate,
                # Associate the new RegularUser with the Supervisor's company
                company=Company.objects.get(id=company_id),
                regular_user=True  # Indicate this user as a RegularUser
                # Additional fields setup
            )

            # Set necessary RegularUser permissions or roles

            # Handle success or redirect
            return HttpResponse("Regular user created successfully")
        else:
            # Handle unauthorized access or show an error message
            return HttpResponse("Permission denied")

    