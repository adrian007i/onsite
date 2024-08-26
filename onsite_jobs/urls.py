from django.contrib import admin 
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("app.public.urls")),
    path('user/', include("app.user.urls")),
    path('recuiter/', include("app.recuiter.urls")),
]
