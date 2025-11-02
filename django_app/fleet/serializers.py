from rest_framework import serializers
from .models import Aircraft

class AircraftSerializer(serializers.ModelSerializer):
    tsn = serializers.ReadOnlyField()  # Property TSN wird mit ausgegeben

    class Meta:
        model = Aircraft
        fields = ["id", "manufacturer", "type", "date_of_manufacture", "tfh", "tsn", "dow", "mtw"]
