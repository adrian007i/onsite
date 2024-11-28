from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.db import IntegrityError 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout ,get_user_model
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from app.decorators import role_required
from django.db.models import Q
from django.core.exceptions import ValidationError
from app.utils import generate_file_name
from dotenv import load_dotenv
import boto3
import os


from app.models.user import User
from app.models.job_title import JobTitle
from app.models.location import Location
from app.models.department import Department
from app.models.job import JobHead, JobDetail
from app.models.saved import Saved
from app.models.applicant import Applicant

load_dotenv() 

def index(request):
    # TODO - if user is logged in, provide their recommendations, else provide new listings
    jobs = JobHead.objects.order_by('-id')[0:10] 
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
        
    u = User()
    u.email = request.POST.get("email").strip()
    u.first_name = request.POST.get("first_name").strip()
    u.last_name = request.POST.get("last_name").strip() 
    u.role = request.POST.get("role")
    u.company =  request.POST.get("company") 

    if request.POST.get("location"):
        u.location_id = request.POST.get("location") 
    
    if request.POST.get("headline"):
        u.headline_id = request.POST.get("headline")
    
    if request.POST.get("password"):
        u.password= make_password(request.POST.get("password")) 

    if "resume_logo" in request.FILES:
        u.resume_logo = generate_file_name() +"_"+ str(request.FILES.get("resume_logo")) 
     
    try:
        u.full_clean()  

        try:
            obj = boto3.client("s3",aws_access_key_id=os.getenv("AWS_KEY"),  aws_secret_access_key= os.getenv("AWS_SECRET"), region_name="us-east-1")  
            obj.upload_fileobj(request.FILES.get("resume_logo"), "onsite-job", u.resume_logo)
        except Exception as e:   
            return JsonResponse({"resume_logo" : "Could not attach! Try Later"} , status=400)
 
        u.save()

        auth_login(request,u)

        if u.role == "recruiter":
            return JsonResponse({"redirect" : "/recruiter/dashboard"}) 
        else:
            return JsonResponse({"redirect" : "/jobs"})
      
    except ValidationError as e:
        print(e.message_dict)
        return JsonResponse(e.message_dict , status=400) 
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
    return render(request , "public/jobs.html", {"jobs" : jobs})  

def jobs(request): 

    try:
        query = Q() 


        if "job_title" in request.GET and request.GET["job_title"] != "": 
            query &= Q(title__name__icontains=request.GET["job_title"])

        if "location" in request.GET and request.GET["location"] != "": 
            query &= Q(location_id=request.GET["location"])
        
        if "page" in request.GET: 
            page = int(request.GET["page"]) - 1
 

        jobs = JobHead.objects.filter(query).order_by('id')
        jobs_count = jobs.count()  
        jobs = jobs[page * 10 : (page * 10) + 10]

    except Exception as e:   
        return HttpResponseRedirect('/jobs?page=1&job_title=&location=')
 
    if len(jobs) != 0:
        
        pages = []

        # pages before
        for i in range(page+1 ,page - 2, -1): 
            if i < 1:
                break
            pages.append(i)   

        last = -(-jobs_count // 10) + 1

        # pages after
        for j in range(page+2, page + 4): 
            if j  == last:
                break 

            pages.append(j)
        
        pages.sort() 

        last_page =  False
        if page + 2 == last:
            last_page = True

    else:
        pages = []
        last_page = True
 
    return render(request , 
                  "public/jobs.html", 
                  {"jobs" : jobs, 
                   "count": jobs_count, 
                   "pages":pages,
                   "last_page" : last_page
                   }) 

def job(request,id,title): 

    job_saved = False
    job_applied = False 

    if request.user.is_authenticated:
        saved = Saved.objects.filter(Q(user_id = request.user.id) & Q(job_id = id)).first() 
        if saved:
            job_saved = True

        applied = Applicant.objects.filter(Q(user_id = request.user.id) & Q(job_id = id)).first()
        if applied:
            job_applied = True

    try:
        job = JobDetail.objects.get(job_head_id = id)
    except Exception as e:
        job = None  
 
 
    return render(request , "public/job.html", {"jd" : job, "applied" : job_applied, "saved":job_saved}) 

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
        companies = companies.filter(company__icontains=search_value) | companies.filter(location__name__icontains=search_value)

    # Apply sorting and pagination
    companies = companies.order_by(order_field)[start:start + length]

    
 
    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': list(companies)
    } 
 
    return JsonResponse (response)  
