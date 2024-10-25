from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from app.decorators import role_required
from django.http import JsonResponse


from app.models.applicant import Applicant
from app.models.saved import Saved

role = "user"

@login_required
@role_required(role)
def applications(request):
    return render(request , "user/applications.html") 

@login_required
@role_required(role)
def ajax_applications(request): 
    
    draw = int(request.POST.get('draw', 0))
    start = int(request.POST.get('start', 0))
    length = int(request.POST.get('length', 10))
    
    # Get the column and direction for sorting
    order_column = int(request.POST.get('order[0][column]', 0))
    order_dir = request.POST.get('order[0][dir]', 'asc')
    
    # Get search value
    search_value = request.POST.get('search[value]', '')

    # Columns data (name, email, etc.)
    columns = ["job_id","job__title__name" ,"created_on__date"]
    
    # Order by the requested column and direction
    order_field = columns[order_column]
    if order_dir == 'desc':
        order_field = '-' + order_field

    # Query users
    listings = Applicant.objects.filter(user_id = request.user.id).values("job_id","job__title__name","job__location__name", "job__salary_min", "job__salary_max", "created_on__date")
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
def saved(request):
    return render(request , "user/saved.html") 

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
     
@login_required
@role_required(role)
def ajax_save(request,id):

    try:
        app = Saved()
        app.user_id = request.user.id
        app.job_id = id
        app.save()
        return JsonResponse({}, status=200)
    except Exception as e:
        print(str(e))
        return JsonResponse({"server" : "Something went wrong. Try Later!"} , status=400)
     