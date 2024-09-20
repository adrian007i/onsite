from django.urls import path

from . import views

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"), 
    path("new_job", views.new_job, name="listings"),
    path("listings", views.listings, name="listings"),
    path("applicants", views.applicants, name="applicants")
]