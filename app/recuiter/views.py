from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from app.decorators import role_required
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse 
from app.models.job import JobHead, JobDetail
from app.utils import *

role = "recruiter"

@login_required
@role_required(role)
def dashboard(request): 
    return render(request , "recruiter/dashboard.html") 

@login_required
@role_required(role)
def view_job(request, job_id): 
    job = JobHead.objects.get(id = job_id) 
    return render(request , "recruiter/job_template.html", {"job": job}) 
    

@login_required
@role_required(role)
def edit_job(request, job_id): 
    job = JobHead.objects.get(id = job_id) 
    return render(request , "recruiter/job_template.html", {"job": job}) 

@login_required
@role_required(role)
def new_job(request): 
    return render(request , "recruiter/job_template.html") 

@login_required
@role_required(role)
def listings(request):
    return render(request , "recruiter/listings.html") 

@login_required
@role_required(role)
def listings_ajax(request):
    
    draw = int(request.POST.get('draw', 0))
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))
    
    # Get the column and direction for sorting
    order_column = int(request.POST.get('order[0][column]', 0))
    order_dir = request.POST.get('order[0][dir]', 'asc')
    
    # Get search value
    search_value = request.POST.get('search[value]', '')

    # Columns data (name, email, etc.)
    columns = ['id', 'experience_level']
    
    # Order by the requested column and direction
    order_field = columns[order_column]
    if order_dir == 'desc':
        order_field = '-' + order_field

    # Query users
    listings = JobHead.objects.all().values("id","experience_level","salary_min", "salary_max" , "active_from", "active_to")

    # Get total count before filtering
    total_records = listings.count()

    # Filter by search value if provided
    if search_value:
        listings = listings.filter(experience_level__icontains=search_value) 

    # Apply sorting and pagination
    listings = listings.order_by(order_field)[start:start + length]

    
 
    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': list(listings)
    } 

    print(listings)
    return JsonResponse (response)  

@login_required
@role_required(role)
def applicants(request):
    return render(request , "recruiter/applicants.html") 


@login_required
@role_required(role)
def new_job_ajax(request):  
 
    try:   
        if request.POST.get("id"): 
            jh = JobHead.objects.get(id = request.POST.get("id"))
        else:
            jh = JobHead()  

        print(request.POST)
 
        # print(request.POST['summary'])

        jh.title_id = request.POST.get('title')
        jh.location_id = request.POST.get('location')
        jh.department_id = request.POST.get('department')
        jh.salary_min = formatNumber(request.POST.get('salary_min'))
        jh.salary_max = formatNumber(request.POST.get('salary_max'))
        jh.experience_level = request.POST.get('experience_level')
        jh.active_from = formatDate(request.POST.get('active_from'))
        jh.active_to = formatDate(request.POST.get('active_to'))
            
        jh.save()
        
        if request.POST.get("id"): 
            jd = JobDetail.objects.filter(job_head_id = jh.id).first()
        else:
            jd = JobDetail()
            jd.job_head_id = jh.id 
 
        jd.summary = request.POST.get('summary')
        jd.duties = request.POST.get('duties')
        jd.qualifications = request.POST.get('qualifications')
        jd.compensation = request.POST.get('compensation')
        jd.save()
        
        print
        return JsonResponse ({"job_id" : jh.id}) 
        
 

    except Exception as e: 
        print(str(e))
        return JsonResponse({"server" : "Something went wrong. Try Later!"} , status=400)
 
