from rest_framework import serializers 
from Security_Cube_app.models import Games 
from .models import Plan, Subscription




class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer()
    class Meta:
        model = Subscription
        fields = '__all__'




