from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.user_login, name="login"),
    path("login_ajax", views.login_ajax),
    path("logout", views.user_logout, name="logout"),
    path("register", views.register, name="register"),
    path("register_ajax", views.register_ajax,),

    path("companies", views.companies, name="companies"),
    path("jobs", views.jobs, name="jobs"), 
    path("profile", views.profile, name = "profile"),
    path("profile_ajax", views.profile_ajax,),

    path("search_location_ajax", views.search_location_ajax, ),
    path("search_job_title_ajax", views.search_job_title_ajax,),
] 