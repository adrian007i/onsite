from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from app.decorators import role_required

role = "user"

@login_required
@role_required(role)
def profile(request): 
    return render(request , "public/register.html") 

@login_required
@role_required(role)
def applications(request):
    return render(request , "public/companies.html") 

@login_required
@role_required(role)
def saved(request):
    return render(request , "public/companies.html") 
