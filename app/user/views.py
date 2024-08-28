from django.shortcuts import render
from django.http import HttpResponse 
 

def profile(request): 
    return render(request , "public/register.html") 

def applications(request):
    return render(request , "public/companies.html") 

def saved(request):
    return render(request , "public/companies.html") 
