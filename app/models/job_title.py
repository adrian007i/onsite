from django.db import models
from app.models.user import * 

class JobTitle(models.Model):
    name = models.CharField(max_length=100, unique=True) 

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]