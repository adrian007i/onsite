ROLE_CHOICES = (
        ("user", "user"),
        ("recruiter", "recruiter"), 
)

from django.db import models
from django.contrib.auth.models import AbstractUser

class UserProfile(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES , default = "user")   

    # def __str__(self):
    #     return f'{self.user.username} - {self.role}'