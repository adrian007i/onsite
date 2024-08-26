from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.user_login, name="login"),
    path("logout", views.user_logout, name="logout"),
    path("register", views.user_signup, name="register"),
    path("companies", views.companies, name="companies"),
    path("jobs", views.jobs, name="jobs"), 
]