from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect


def index(request):
     return HttpResponseRedirect("/jobs") 

def user_login(request):
    return render(request , "public/login.html") 

def user_logout(request):
    return HttpResponse("logout")

def user_signup(request): 
    return render(request , "public/register.html") 

def companies(request):
    return render(request , "public/companies.html") 

def jobs(request):
    return render(request , "public/jobs.html")  