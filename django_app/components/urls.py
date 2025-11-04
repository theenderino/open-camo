from rest_framework.routers import DefaultRouter
from .views import ComponentViewSet, RequirementViewSet, InstallationViewSet

# -------------------------------
# DefaultRouter erstellt automatisch REST-API Endpunkte
# - GET /components/          -> Liste aller Komponenten
# - POST /components/         -> Neue Komponente anlegen
# - GET /components/{id}/     -> Einzelne Komponente abrufen
# - PUT/PATCH /components/{id}/ -> Komponente aktualisieren
# - DELETE /components/{id}/  -> Komponente löschen
# 
# Entsprechend für requirements und installations
# -------------------------------
router = DefaultRouter()
router.register(r"components", ComponentViewSet)
router.register(r"requirements", RequirementViewSet)
router.register(r"installations", InstallationViewSet)

# -------------------------------
# Die URL Patterns für die App werden aus dem Router übernommen
# -------------------------------
urlpatterns = router.urls
