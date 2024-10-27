from django.urls import path

from . import views

urlpatterns = [
    path("dashboard", views.dashboard, name="dashboard"), 
    path("view_job/<int:job_id>", views.view_job, name="view_job"),
    path("edit_job/<int:job_id>", views.edit_job, name="edit_job"),
    path("new_job", views.new_job, name="new_job"),
    path("new_job_ajax", views.new_job_ajax ),
    path("listings", views.listings, name="listings"),
    path("listings_ajax", views.listings_ajax ),
    path("applicants", views.applicants, name="applicants"),
    path("applications_ajax", views.applications_ajax)
]