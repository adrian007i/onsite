from django.db import models 

class Location(models.Model):
    name = models.CharField(max_length=100, unique=True) 
    loc_tyep = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
