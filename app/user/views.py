from django.shortcuts import render
from django.http import HttpResponse

def profile(request):
    return HttpResponse("my profile")

def apply(request):
    return HttpResponse("apply to a job")

def applications(request):
    return HttpResponse("list of my applications ")

def saved(request):
    return HttpResponse("list of saved jobs")