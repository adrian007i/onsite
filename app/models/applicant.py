from django.db import models
from app.models.user import *
from app.models.job import JobHead

class Applicant(models.Model):
    job = models.OneToOneField(JobHead, on_delete=models.CASCADE, related_name="applicant_job")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="applicanat_user")