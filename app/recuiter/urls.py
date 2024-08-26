from django.urls import path

from . import views

urlpatterns = [
    path("dashboard", views.dashboard, name="profile"),
    path("post_job", views.post_job, name="apply"),
    path("applicants", views.applicant_pool, name="applications"), 
    path("payments", views.payments, name="saved"), 
]