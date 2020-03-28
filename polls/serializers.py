from .models import Stat
from rest_framework import serializers

class StatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Stat
        fields = ['user','sessionID','time', 'hr', 'rr']
