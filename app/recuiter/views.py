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
 
