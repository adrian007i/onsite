from django.urls import path

from . import views

urlpatterns = [
    # path("apply", views.apply, name="apply"),
    path("applications", views.applications, name="applications"), 
    path("saved", views.saved, name="saved"), 
    path("apply_ajax/<int:id>", views.ajax_apply), 
    path("save_ajax/<int:id>", views.ajax_save), 
    path("applications_ajax", views.ajax_applications), 
]