from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from components.urls import router as components_router

# -------------------------------
# Home-View: Landing Page für API
# -------------------------------
def home(request):
    """
    Root-Endpunkt ("/")
    - Liefert eine einfache Willkommensnachricht
    - Weist auf Fleet-API und Components-API hin
    """
    return HttpResponse(
        "Welcome to Open Camo! Visit /api/aircraft/ for fleet data "
        "and /api/components/ for components."
    )

# -------------------------------
# URL Patterns
# -------------------------------
urlpatterns = [
    # Landing Page
    path("", home, name="home"),

    # Admin-Oberfläche
    path("admin/", admin.site.urls),

    # Fleet-API (Aircraft)
    path("", include("fleet.urls")),  # REST-Endpunkte z.B. /api/aircraft/

    # Components-API (Components, Requirements, Installationen)
    path("api/", include(components_router.urls)),
]

# -------------------------------
# Hinweise:
# - components_router enthält automatisch alle Endpunkte für:
#   /components/, /requirements/, /installations/
# - Fleet-URLs bleiben unverändert
# -------------------------------
