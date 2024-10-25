from django.urls import path

from . import views

urlpatterns = [
    # path("apply", views.apply, name="apply"),
    path("applications", views.applications, name="applications"), 
    path("saved", views.saved, name="saved"), 
    path("apply_ajax/<int:id>", views.apply_ajax), 
    path("save_ajax/<int:id>", views.save_ajax), 
    path("applications_ajax", views.applications_ajax), 
    path("saved_ajax", views.saved_ajax), 
]