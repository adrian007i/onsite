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

    jh = None
    jd = None
    
    print(formatDate(request.POST.get('active_to')))
    try:   

        jh = JobHead.objects.create(
        title_id = request.POST.get('title'),
        location_id = request.POST.get('location'), 
        department_id = request.POST.get('department'),
        posted_on = request.POST.get('posted_on'),
        salary_min = formatNumber(request.POST.get('salary_min')),
        salary_max = formatNumber(request.POST.get('salary_max')),
        experience_level = request.POST.get('experience_level'),
        active_from = formatDate(request.POST.get('active_from')),
        active_to = formatDate(request.POST.get('active_to'))) 

        if jh: 
            jd = JobDetail.objects.create(
            job_head_id = jh.id,
            summary =  request.POST.get('summary'),
            duties = request.POST.get('duties'), 
            qualifications = request.POST.get('qualifications'),
            compensation = request.POST.get('compensation'))

        if jh and jd:
            return JsonResponse ({}) 
        
        else:
            jh.delete()
            jd.delete()
 

    except Exception as e: 
        print(str(e))
        return JsonResponse({"server" : "Something went wrong. Try Later!"} , status=400)
 
