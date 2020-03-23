from .models import Dummy
from rest_framework import serializers

class DummySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Dummy
        fields = ['time', 'hr', 'rr']
