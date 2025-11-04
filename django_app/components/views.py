from rest_framework import viewsets
from .models import Component, Requirement, Installation
from .serializers import ComponentSerializer, RequirementSerializer, InstallationSerializer
from django.utils import timezone

# -------------------------------
# ViewSet für Requirements
# -------------------------------
class RequirementViewSet(viewsets.ModelViewSet):
    """
    CRUD für Requirements (z.B. Inspection, Overhaul)
    """
    queryset = Requirement.objects.all()
    serializer_class = RequirementSerializer

# -------------------------------
# ViewSet für Components
# -------------------------------
class ComponentViewSet(viewsets.ModelViewSet):
    """
    CRUD für Components (Bauteile)
    - Requirements werden read-only verschachtelt angezeigt
    """
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

# -------------------------------
# ViewSet für Installationen (Einbau/Ausbau)
# -------------------------------
class InstallationViewSet(viewsets.ModelViewSet):
    """
    CRUD für Installationen:
    - create: Einbau -> TSI auf 0 setzen
    - update/partial_update: Ausbau -> TSO auf TSN zum Zeitpunkt des Ausbaus setzen
    """

    queryset = Installation.objects.all()
    serializer_class = InstallationSerializer

    def perform_create(self, serializer):
        """
        Beim Einbau einer Komponente:
        - Installation speichern
        - TSI (Time Since Installation) der Komponente auf 0 zurücksetzen
        """
        installation = serializer.save()
        comp = installation.component
        comp.tsi = 0
        comp.save()

    def perform_update(self, serializer):
        """
        Beim Aktualisieren einer Installation:
        - Wenn removed_at gesetzt wird (Ausbau):
          - TSO (Time Since Overhaul) auf TSN zum Zeitpunkt des Ausbaus setzen
        """
        installation = serializer.save()
        comp = installation.component

        if installation.removed_at and installation.removed_at <= timezone.now().date():
            comp.tso = comp.tsn
            comp.save()
