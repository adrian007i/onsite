from django.db import models
from app.models.user import *
from app.models.job import JobHead

class Saved(models.Model):
    job = models.OneToOneField(JobHead, on_delete=models.CASCADE, related_name="job")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")