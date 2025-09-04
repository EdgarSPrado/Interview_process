
from django.contrib import admin
from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name="home"), 
    path("technical-evaluation/", views.technical_evaluation, name="technical_evaluation"),
    path("guardar-evaluacion/", views.guardar_evaluacion, name="guardar_evaluacion"),
]
if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)