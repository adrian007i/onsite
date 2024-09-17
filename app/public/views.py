from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.core.exceptions import BadRequest
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout ,get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from app.decorators import role_required

from app.models.user import *
from app.models.job import *
from app.models.job_title import JobTitle
from app.models.location import Location

def index(request):
    if request.user.is_authenticated and request.user.role == "recruiter":
        return HttpResponseRedirect("/recruiter/dashboard")
    else:
        return HttpResponseRedirect("/jobs")
         
def search_job_title_ajax(request): 

    try:  
        if request.GET.get("query"):
            job_titles = JobTitle.objects.filter(name__contains =  request.GET.get("query").lower()).values()
            return JsonResponse (({'job_titles' : list(job_titles)}) ) 
      
    except Exception as e:
        return JsonResponse({"server" : "Something went wrong. Try Later!"} , status=400)

def search_location_ajax(request):  

    try:  
        if request.GET.get("query"):
            job_titles = Location.objects.filter(name__startswith  =  request.GET.get("query").lower()).values()
            return JsonResponse (({'locations' : list(job_titles)}) ) 
    except Exception as e:
        return JsonResponse({"server" : "Something went wrong. Try Later!"} , status=400)

def user_login(request): 
    return render(request , "public/login.html") 

def login_ajax(request):
     
    try:
        user = authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))

        if user:
            auth_login(request,user)
            return JsonResponse ({'redirect' : f'/jobs'})
        else:
            return JsonResponse({"server" : "Invalid Credentials"} , status=400) 
        
    except Exception as e:
        return JsonResponse({"server" : "Something went wrong. Try Later!"} , status=400)
 

def user_logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))

def register(request): 
    return render(request , "public/register.html") 

def register_ajax(request):

    try: 
        user = User.objects.create(
        email = request.POST.get("email"), 
        first_name = request.POST.get("first_name"), 
        last_name = request.POST.get("last_name"), 
        headline = request.POST.get("headline"), 
        role = request.POST.get("role"),
        company = request.POST.get("company"),
        password= make_password(request.POST.get("password"))) 
              
        auth_login(request,user)

        if user.role == "recruiter":
            return HttpResponseRedirect("/recruiter/dashboard")
        else:
            return HttpResponseRedirect("/jobs") 
     
    except IntegrityError as ie: 
        return JsonResponse({"email" : "This email already exist!"} , status=400)
    except Exception as e:
        return JsonResponse({"server" : "Something went wrong. Try Later!"} , status=400)
    
@login_required 
def profile(request):
    for f in request.user._meta.fields:
        print(f.name, getattr(request.user, f.name))
    return render(request , "public/profile.html")

@login_required
def profile_ajax(request):

    try: 
        user = User.objects.get(id = request.user.id) 

        user.email = request.POST.get("email")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.headline = request.POST.get("headline")

        
        if request.user.role == "recruiter":
            user.company = request.POST.get("company")

        if request.POST.get("password"):
            user.password= make_password(request.POST.get("password"))
            auth_login(request,user)

        user.save()
               
        return JsonResponse ({})
     
    except IntegrityError as ie: 
        return JsonResponse({"email" : "This email already exist!"} , status=400)
    except Exception as e:
        return JsonResponse({"server" : "Something went wrong. Try Later!"} , status=400)
    

def companies(request):
    return render(request , "public/companies.html") 

def jobs(request):
    return render(request , "public/jobs.html")  