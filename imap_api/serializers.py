from rest_framework import serializers

from imap_api.models import *


class BatimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batiment
        fields = '__all__'


class SalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salle
        fields = '__all__'


class CheckPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckPoint
        fields = '__all__'


class CableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cable
        fields = '__all__'


class EtageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etage
        fields = '__all__'




