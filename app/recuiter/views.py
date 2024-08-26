from django.shortcuts import render
from django.http import HttpResponse

def dashboard(request):
    return HttpResponse("my profile")

def post_job(request):
    return HttpResponse("apply to a job")

def applicant_pool(request):
    return HttpResponse("list of my applications ")

def payments(request):
    return HttpResponse("list of saved jobs")