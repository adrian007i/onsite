from django.db import models
from app.models.user import User
from app.models.job import JobHead

class Saved(models.Model):
    job = models.ForeignKey(JobHead, on_delete=models.SET_NULL,null=True,  related_name="job")
    user = models.ForeignKey(User, on_delete=models.SET_NULL,null=True,  related_name="user")
    created_on = models.DateTimeField(auto_now_add=True, null=True)

    # ensures the user cant save the same job multiple times
    class Meta:
        unique_together = ('job', 'user') 