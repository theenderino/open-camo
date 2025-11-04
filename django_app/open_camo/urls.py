from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from rest_framework import routers

# Importiere deine ViewSets
from fleet.views import AircraftViewSet
from components.views import PartViewSet

# Router für REST-API-Endpunkte
router = routers.DefaultRouter()
router.register(r'aircraft', AircraftViewSet)
router.register(r'parts', PartViewSet)

def home(request):
    return HttpResponse("Welcome to Open Camo! Visit /api/ for available endpoints.")

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)), # 👈 REST API für alle Apps
    path("", include("fleet.urls")),
    path("", include("components.urls")),  
]
