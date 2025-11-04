from rest_framework import serializers
from .models import Component, Requirement, Installation

# -------------------------------
# Serializer für Requirement
# -------------------------------
class RequirementSerializer(serializers.ModelSerializer):
    """
    Serialisiert Requirement-Objekte.
    - Alle Felder werden ausgegeben.
    """
    class Meta:
        model = Requirement
        fields = "__all__"

# -------------------------------
# Serializer für Component
# inklusive der zugeordneten Requirements (read-only)
# -------------------------------
class ComponentSerializer(serializers.ModelSerializer):
    """
    Serialisiert Component-Objekte.
    - Die zugeordneten Requirements werden als verschachteltes read-only Feld angezeigt.
    """
    requirements = RequirementSerializer(many=True, read_only=True)

    class Meta:
        model = Component
        fields = "__all__"

# -------------------------------
# Serializer für Installation
# -------------------------------
class InstallationSerializer(serializers.ModelSerializer):
    """
    Serialisiert Installationen von Komponenten.
    - component_id wird für POST/PATCH verwendet
    - component als verschachteltes Objekt read-only für GET-Ausgaben
    """
    # Verschachtelte Darstellung der Komponente beim Abrufen
    component = ComponentSerializer(read_only=True)
    # Für POST/PATCH: Komponente via ID setzen
    component_id = serializers.PrimaryKeyRelatedField(
        queryset=Component.objects.all(), source='component', write_only=True
    )

    class Meta:
        model = Installation
        fields = [
            'id',
            'aircraft',
            'component',      # read-only verschachtelt
            'component_id',   # write-only für API Eingaben
            'installed_at',
            'removed_at',
        ]
