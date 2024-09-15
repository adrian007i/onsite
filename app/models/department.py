from django.db import models
from app.models.user import * 

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True) 