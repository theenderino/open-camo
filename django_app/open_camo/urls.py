from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

# Import Router aus Components
from components.urls import router as components_router

def home(request):
    return HttpResponse(
        "Welcome to Open Camo! "
        "Visit /api/aircraft/ for fleet data "
        "and /api/components/ for components."
    )

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("", include("fleet.urls")),               # Fleet API
    path("api/", include(components_router.urls)), # Components API
]
