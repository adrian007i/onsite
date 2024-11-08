from django.db import models
from app.models.user import User
from app.models.job import JobHead

class Applicant(models.Model):
    job = models.OneToOneField(JobHead, on_delete=models.SET_NULL, null=True, related_name="applicant_job")
    user = models.OneToOneField(User, on_delete=models.SET_NULL,null=True,related_name="applicanat_user")
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    # ensures the user cannot apply to the same job multiple times
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['job_id', 'user_id'], name='unique_applicant_job_user')
        ]