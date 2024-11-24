from django.contrib import admin
from app.models.user import User
from app.models.applicant import Applicant
from app.models.saved import Saved
# Register your models here.

admin.site.register(User)
admin.site.register(Applicant)
admin.site.register(Saved)

