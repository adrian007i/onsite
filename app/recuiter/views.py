from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from app.decorators import role_required
from django.http import HttpResponseRedirect, JsonResponse 
from app.utils import *
from django.db.models import Q
from django.db.models import Count

from app.models.job import JobHead, JobDetail
from app.models.applicant import Applicant 
from datetime import date,timedelta



role = "recruiter"

@login_required
@role_required(role)
def dashboard(request): 

    # jobs posted stats
    jobs = JobHead.objects.filter(created_by_id = request.user.id)
    today = date.today()
    total = jobs.count()
    active = jobs.filter(Q(draft = False) & (Q(active_from__lte=today) & Q(active_to__gte=today))).count()

    # application stats
    applications = Applicant.objects.filter(job__created_by_id = request.user.id)
    total_applications = applications.count()
    applicants = applications.values_list('user_id', flat=True).distinct().count()

    # charts 
    # jobs by department
    jobs_by_department = jobs.values("department_id","department__name").annotate(count=Count("department_id")).order_by("-count")[:10]

    # job applications by month
    one_year_ago = datetime.datetime.now(datetime.timezone.utc) + timedelta(days=-182) 
    applications_by_month = applications.filter(created_on__gte = one_year_ago).values("created_on__month").annotate(count = Count("created_on__month"))
    return render(
        request , 
        "recruiter/dashboard.html", 
            {
                "total":total, 
                "active":active, 
                "applications": total_applications, 
                "applicants":applicants,
                "jobs_by_department":jobs_by_department,
                "applications_by_month":applications_by_month
            }

    )

@login_required
@role_required(role)
def view_job(request, job_id): 
    try:
        job = JobHead.objects.get(Q(id = job_id) & Q(created_by_id = request.user.id))
        return render(request , "recruiter/job_template.html", {"job": job}) 
    except:
        return HttpResponseRedirect('/')
    

@login_required
@role_required(role) 
def edit_job(request, job_id): 
    try:
        job = JobHead.objects.get(Q(id = job_id) & Q(created_by_id = request.user.id))
        return render(request , "recruiter/job_template.html", {"job": job}) 
    except:
        return HttpResponseRedirect('/')

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
    listings = JobHead.objects.filter(created_by_id = request.user.id).values("id","experience_level","salary_min", "salary_max" , "active_from", "active_to","title__name", "department__name")
    # Get total count before filtering
    total_records = listings.count()

    # Filter by search value if provided
    if search_value:
        listings = listings.filter(id__icontains=search_value) | listings.filter(title__name__icontains=search_value)

    # Apply sorting and pagination
    listings = listings.order_by(order_field)[start:start + length]

    
 
    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': list(listings)
    } 
 
    return JsonResponse (response)  

@login_required
@role_required(role)
def applicants(request):
    return render(request , "recruiter/applicants.html") 

@login_required
@role_required(role)
def applications_ajax(request): 
    
    draw = int(request.POST.get('draw', 0))
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))
    
    # Get the column and direction for sorting
    order_column = int(request.POST.get('order[0][column]', 0))
    order_dir = request.POST.get('order[0][dir]', 'asc')
    
    # Get search value
    search_value = request.POST.get('search[value]', '')

    # Columns data (name, email, etc.)
    columns = [
        "job_id","job__title__name","job__location__name", "job__salary_min", 
        "job__salary_max", "created_on__date","user__first_name","user__last_name",
        "user__location__name","user__headline__name"
        ]
    
    # Order by the requested column and direction
    order_field = columns[order_column]
    if order_dir == 'desc':
        order_field = '-' + order_field

    # Query users
    listings = Applicant.objects.filter(job__created_by = request.user.id).values(*columns)
    # Get total count before filtering
    total_records = listings.count()

    # Filter by search value if provided
    if search_value:
        listings = listings.filter(job__title__name__icontains=search_value)

    # Apply sorting and pagination
    listings = listings.order_by(order_field)[start:start + length]
 
    response = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
        'data': list(listings)
    }  
    return JsonResponse (response)  




@login_required
@role_required(role)
def new_job_ajax(request):  
 
    try:   
        if request.POST.get("id"): 
            jh = JobHead.objects.get(id = request.POST.get("id"))
        else:
            jh = JobHead()  
 
        jh.title_id = request.POST.get('title')
        jh.location_id = request.POST.get('location')
        jh.department_id = request.POST.get('department')
        jh.salary_min = formatNumber(request.POST.get('salary_min'))
        jh.salary_max = formatNumber(request.POST.get('salary_max'))
        jh.experience_level = request.POST.get('experience_level')
        jh.active_from = formatDate(request.POST.get('active_from'))
        jh.active_to = formatDate(request.POST.get('active_to'))
        jh.created_by_id = request.user.id
            
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
         
        return JsonResponse ({"job_id" : jh.id}) 
        
 

    except Exception as e:  
        return JsonResponse({"server" : "Something went wrong. Try Later!"} , status=400)
 
