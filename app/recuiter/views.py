from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from app.decorators import role_required

role = "recruiter"

@login_required
@role_required(role)
def dashboard(request): 
    return render(request , "recruiter/dashboard.html") 

@login_required
@role_required(role)
def post_job(request): 
    return render(request , "public/post_job.html") 

@login_required
@role_required(role)
def listings(request):
    return render(request , "recruiter/listings.html") 

@login_required
@role_required(role)
def applicants(request):
    return render(request , "recruiter/applicants.html") 

 
