from django.db import models
from django.contrib.auth import models as auth_models  
from app.models.job_title import JobTitle
from app.models.location import Location
from app.utils import error_messages
ROLE_CHOICES = (
        ("user", "user"),
        ("recruiter", "recruiter"), 
)

class UserManager(auth_models.BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password=password)
        user.is_superuser = user.is_staff = True
        user.save(using=self._db)
        return user

class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(unique=True, error_messages=error_messages) 
    headline = models.ForeignKey(JobTitle, on_delete=models.SET_NULL,null=True, error_messages=error_messages)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL,blank=True, null=True, error_messages=error_messages)
    other_headline = models.CharField(max_length=250, null=True, blank=True, error_messages=error_messages)
    company = models.CharField(max_length=250, null=True, default = None, blank=True, error_messages=error_messages) 
    first_name = models.CharField(max_length=30, blank=False, error_messages=error_messages)
    last_name = models.CharField(max_length=30, blank=False, error_messages=error_messages) 
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False) 
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True) 
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="user")
    resume_logo = models.CharField(max_length=150, null=False, blank=False, error_messages=error_messages)
    password = models.CharField(max_length=100, null=False,blank=False, error_messages=error_messages)

    
     

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'
        ordering = ('id', ) 

    def __unicode__(self):
        return u'{0} ({1})'.format(self.get_full_name(), self.email)

    def get_short_name(self):
        return self.first_name

    def get_full_name(self):
        return u'{0} {1}'.format(self.first_name, self.last_name)