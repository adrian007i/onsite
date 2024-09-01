from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse

from app.models import *
from django.contrib.auth import get_user_model

def index(request):
     return HttpResponseRedirect("/jobs") 

def user_login(request):
    return render(request , "public/login.html") 

def user_logout(request):
    return HttpResponse("logout")

def register(request): 
    return render(request , "public/register.html") 

def register_ajax(request):

    try:
        # model = get_user_model() 
        User.objects.create(
        email = request.POST.get("email"), 
        first_name = request.POST.get("first_name"), 
        last_name = request.POST.get("last_name"), 
        headline = request.POST.get("headline"), 
        role = request.POST.get("role"),
        password= request.POST.get("password")
        )
        return JsonResponse({"success" : True})
    except Exception as e:
        print(str(e)) 
        return JsonResponse({"success" : False})
    

def companies(request):
    return render(request , "public/companies.html") 

def jobs(request):
    return render(request , "public/jobs.html")  