from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse
from django.db import IntegrityError
from django.core.exceptions import BadRequest
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout ,get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from app.decorators import role_required

from app.models.user import User
# from app.models.job import 
from app.models.job_title import JobTitle
from app.models.location import Location
from app.models.department import Department
from app.models.job import JobHead, JobDetail

def index(request):
    # TODO - if user is logged in, provide their recommendations, else provide new listings
    jobs = JobHead.objects.order_by('posted_on')[0:10] 
    return render(request , "public/landing.html", {"jobs" : jobs})
         
def search_job_title_ajax(request): 

    try:  
        if request.GET.get("query"):
            job_titles = JobTitle.objects.filter(name__contains =  request.GET.get("query").lower()).values()[:10]
            return JsonResponse (({'data' : list(job_titles)}) ) 
      
    except Exception as e:
        return JsonResponse({"server" : "Something went wrong. Try Later!"} , status=400)

def search_location_ajax(request):  

    try:  
        if request.GET.get("query"):
            job_titles = Location.objects.filter(name__startswith  =  request.GET.get("query").lower()).values()[:10]
            return JsonResponse (({'data' : list(job_titles)}) ) 
    except Exception as e:
        return JsonResponse({"server" : "Something went wrong. Try Later!"} , status=400)

def search_department_ajax(request):  
    try:  
        if request.GET.get("query"):
            departments = Department.objects.filter(name__contains =  request.GET.get("query").lower()).values()[:10]
            return JsonResponse (({'data' : list(departments)}) ) 
      
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
        location_id = request.POST.get("location")
        if not request.POST.get("location"):
            location_id = None 

        user = User.objects.create(
        email = request.POST.get("email"), 
        first_name = request.POST.get("first_name"), 
        last_name = request.POST.get("last_name"), 
        headline_id = request.POST.get("headline"), 
        role = request.POST.get("role"),
        company = request.POST.get("company"),
        location_id = location_id,
        password= make_password(request.POST.get("password"))) 
              
        auth_login(request,user)

        if user.role == "recruiter":
            return JsonResponse({"redirect" : "/recruiter/dashboard"}) 
        else:
            return JsonResponse({"redirect" : "/jobs"})
     
    except IntegrityError as ie: 
        return JsonResponse({"email" : "This email already exist!"} , status=400)
    except Exception as e: 
        return JsonResponse({"server" : "Something went wrong. Try Later!"} , status=400)
    
@login_required 
def profile(request): 
    return render(request , "public/profile.html")

@login_required
def profile_ajax(request):

    try: 
        user = User.objects.get(id = request.user.id) 

        location_id = request.POST.get("location")
        if not request.POST.get("location"):
            location_id = None 

        user.email = request.POST.get("email")
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.headline_id = request.POST.get("headline")
        user.location_id = location_id
        
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

def jobs_listing(request, id):
    jobs = JobHead.objects.all() 
    jd = JobDetail.objects.get(job_head_id = id) 
    return render(request , "public/jobs.html", {"jobs" : jobs , "jd" : jd})  

def jobs(request): 
    return render(request , "public/landing.html")  


def companies_ajax(request): 
    
    draw = int(request.POST.get('draw', 0))
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))
    
    # Get the column and direction for sorting
    order_column = int(request.POST.get('order[0][column]', 0))
    order_dir = request.POST.get('order[0][dir]', 'asc')
    
    # Get search value
    search_value = request.POST.get('search[value]', '')

    # Columns data (name, email, etc.)
    columns = ['company', 'location_id']
    
    # Order by the requested column and direction
    order_field = columns[order_column]
    if order_dir == 'desc':
        order_field = '-' + order_field

    # Query users
    companies = User.objects.filter(company__isnull = False).values("company" , "location__name")

    # Get total count before filtering
    total_records = companies.count()

    # Filter by search value if provided
    if search_value:
        companies = companies.filter(company__icontains=search_value) | companies.filter(locatiion__name__icontains=search_value)

    # Apply sorting and pagination
    companies = companies.order_by(order_field)[start:start + length]

    
 
    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': list(companies)
    } 
 
    return JsonResponse (response)  
