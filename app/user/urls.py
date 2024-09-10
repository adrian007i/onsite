from django.urls import path

from . import views

urlpatterns = [
    # path("apply", views.apply, name="apply"),
    path("applications", views.applications, name="applications"), 
    path("saved", views.saved, name="saved"), 
]