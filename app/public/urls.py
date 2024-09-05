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
] 