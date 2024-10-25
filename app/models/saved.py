from django.db import models
from app.models.user import User
from app.models.job import JobHead

class Saved(models.Model):
    job = models.OneToOneField(JobHead, on_delete=models.CASCADE, related_name="job")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user")
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    # ensures the user cant save the same job multiple times
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['job_id', 'user_id'], name='unique_applicant_jobsave')
        ]