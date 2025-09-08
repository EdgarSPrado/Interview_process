from django.contrib import admin
from django.urls import path
from main import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.login_view, name="login"),  # Login como página principal
    path("home/", views.home, name="home"),   # Home redirigido después de login
    path("technical-evaluation/", views.technical_evaluation, name="technical_evaluation"),
    path("guardar-evaluacion/", views.guardar_evaluacion, name="guardar_evaluacion"),
    path('create-group/', views.create_group_view, name='create_group'),
    path('process/', views.process_view, name='process'),
    path('calendar/admin', views.calendar_admin_view, name='calendar_admin'),
    path('calendar/user', views.calendar_user_view, name='calendar_user'),
    path('calendar/', views.calendar_view, name='calendar'),
    path("api/eventos/", views.eventos_list, name="eventos_list"),
    path("api/eventos/crear/", views.crear_evento, name="crear_evento"),
    path("api/eventos/crear-user/", views.crear_evento_user, name="crear_evento_user"),

]

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
