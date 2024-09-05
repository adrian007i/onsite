from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.core.exceptions import BadRequest
from app.models import *
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout ,get_user_model
from django.contrib.auth.hashers import make_password

def index(request):
     return HttpResponseRedirect("/jobs") 

def user_login(request): 
    return render(request , "public/login.html") 

def login_ajax(request):
     
    try:
        print(request.POST.get("password") , request.POST.get("email"))
        user = authenticate(request, username=request.POST.get("email"), password=request.POST.get("password"))  
        print(user)
        if user:
            auth_login(request,user)
            return JsonResponse ({'redirect' : f'/{user.role}/profile'})
        else:
            return JsonResponse({"server" : "Invalid Credentials"} , status=400) 
        
    except Exception as e:
        return JsonResponse({"server" : "Something went wrong. Try Later!"} , status=400)
 

def user_logout(request):
    return HttpResponse("logout")

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
        password= make_password(request.POST.get("password"))) 
              
        auth_login(request,user)
 
        return JsonResponse ({'redirect' : f'/{user.role}/profile'})
     
    except IntegrityError as ie: 
        return JsonResponse({"email" : "This email already exist!"} , status=400)
    except Exception as e:
        return JsonResponse({"server" : "Something went wrong. Try Later!"} , status=400)
    

def companies(request):
    return render(request , "public/companies.html") 

def jobs(request):
    return render(request , "public/jobs.html")  