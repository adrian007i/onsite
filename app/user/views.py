from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from app.decorators import role_required
from app.models.applicant import Applicant
from django.http import JsonResponse

role = "user"

@login_required
@role_required(role)
def applications(request):
    return render(request , "public/companies.html") 

@login_required
@role_required(role)
def saved(request):
    return render(request , "public/companies.html") 

@login_required
@role_required(role)
def ajax_apply(request,id):

    try:
        app = Applicant()
        app.user_id = request.user.id
        app.job_id = id
        app.save()
        return JsonResponse({}, status=200)
    except Exception as e:
        print(str(e))
        return JsonResponse({"server" : "Something went wrong. Try Later!"} , status=400)
     
