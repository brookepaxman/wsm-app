from .models import Dummy
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class SessionSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Session
        fields = ['user', 'startDate', 'startTime']

class StatSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    sessionID = SessionSerializer()
    class Meta:
        model = Stat
        fields = ['user','sessionID','time', 'hr', 'rr']

class AnalysisSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    sessionID = SessionSerializer()
    class Meta:
        model = Analysis
        fields = ['user','sessionID','tst','avgHR','avgRR', 'dailyHR', 'dailyRR']

class StrippedAnalysisSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()
    sessionID = SessionSerializer()
    class Meta:
        model = Analysis
        fields = ['user','sessionID','tst','avgHR','avgRR', 'dailyHR', 'dailyRR']
