
from django.db import models
from app.models.job_title import JobTitle
from app.models.location import Location
from app.models.department import Department

EXP_LEVEL = (
        ("any", "any"),
        ("internship", "internship"),
        ("entry", "entry"),
        ("associate", "associate"),
        ("mid", "mid"),
        ("senior", "senior"), 
        ("director", "director"),
        ("executive", "executive"),  
) 

class JobHead(models.Model):
    title = models.ForeignKey(JobTitle, on_delete=models.DO_NOTHING)
    other_title =  models.CharField(max_length=255, null=True)
    location = models.ForeignKey(Location, on_delete=models.DO_NOTHING, null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, null=True)
    other_department =  models.CharField(max_length=255, null=True)
    posted_on = models.DateTimeField(auto_now_add=True)
    salary_min = models.IntegerField(null=True)
    salary_max = models.IntegerField(null=True) 
    experience_level =   models.CharField(max_length=15, choices=EXP_LEVEL, default="any")
    active_from = models.DateField(null=True)
    active_to = models.DateField(null=True)
    draft = models.BooleanField(default=False)
    
    # def __str__(self):
    #     return self.title


class JobDetail(models.Model):
    job_head = models.OneToOneField(JobHead, on_delete=models.CASCADE, related_name="details")
    summary = models.TextField()
    duties = models.TextField()
    qualifications = models.TextField()
    compensation = models.TextField()

    def __str__(self):
        return f"Details of {self.job_head.title}"