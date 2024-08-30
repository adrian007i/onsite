from django.shortcuts import render
from django.http import HttpResponseRedirect

def index(request):
     return HttpResponseRedirect("/recruiter/dashboard/") 

def dashboard(request): 
    return render(request , "recruiter/dashboard.html") 

def post_job(request): 
    return render(request , "public/post_job.html") 

def listings(request):
    return render(request , "recruiter/listings.html") 

def applicants(request):
    return render(request , "recruiter/applicants.html") 

def profile(request):
    return render(request , "recruiter/profile.html") 
