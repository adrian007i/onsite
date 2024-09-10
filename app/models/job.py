
from django.db import models

class JobHead(models.Model):
    title = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    posted_on = models.DateTimeField(auto_now_add=True)
    salary_range = models.CharField(max_length=50)
    application_deadline = models.DateTimeField()
    experience_level = models.CharField(max_length=50) 
    
    def __str__(self):
        return self.title


class JobDetails(models.Model):
    job_head = models.OneToOneField(JobHead, on_delete=models.CASCADE, related_name="details")
    summary = models.TextField()
    duties = models.TextField()
    qualifications = models.TextField()
    compensation = models.TextField()

    def __str__(self):
        return f"Details of {self.job_head.title}"