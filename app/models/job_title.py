from django.db import models 

class JobTitle(models.Model):
    name = models.CharField(max_length=100, unique=True) 

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]

    
    def __str__(self):
        return self.name 