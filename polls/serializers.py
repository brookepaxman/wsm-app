from .models import Stat, User, Session, Analysis
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['user_name', 'pub_date']

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
        fields = ['user','sessionID','date','tst','avgHR','avgRR','avgHRdip','minHR','maxHR','minRR','maxRR','numSleepDisruptions']
