# project/urls.py (or your project's urls file)
from django.contrib import admin
from django.urls import path
from mathapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('powercalc/', views.powercalc, name="powercalculator"),
    path('', views.powercalc, name="powercalcroot"),
]