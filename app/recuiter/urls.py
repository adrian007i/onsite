from django.urls import path

from . import views

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"), 
    path("post_job", views.post_job, name="post_job"),
    path("listings", views.listings, name="listings"),
    path("applicants", views.applicants, name="applicants")
]