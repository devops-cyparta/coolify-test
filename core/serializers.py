from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Customer, Level, User 
from django_countries import countries
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
import math             


# Country Serializer 
class CountrySerializer(serializers.BaseSerializer):

    def to_representation(self, obj):
        return str(obj)

    def to_internal_value(self, data):
        if data not in [code for code, name in countries]:
            raise serializers.ValidationError("Invalid country code")
        return data
    
class UserCreateSerializer(BaseUserCreateSerializer):
        country = CountrySerializer()
        class Meta(BaseUserCreateSerializer.Meta):
            fields = ['id', 'first_name', 'username','password','email', 'phone', 'country'] 
        


class UserSerializer(BaseUserSerializer):
    country = serializers.CharField(source='user.country')
    class Meta(BaseUserSerializer.Meta):
        fields = ['id', 'first_name', 'username', 'email', 'phone', 'points', 'date_joined', 'country']



# Level Serializer 
class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level 
        fields = ('name', 'img')

# Customer Serializer 
class CustomerSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name')
    phone = serializers.CharField(source='user.phone', max_length=20)
    email = serializers.EmailField(source='user.email')
    points = serializers.ReadOnlyField(source='user.points')
    date_joined = serializers.ReadOnlyField(source='user.date_joined')
    daily_target = serializers.ReadOnlyField(source='user.daily_target')
    current_level = LevelSerializer(read_only=True, source='user.current_level')
    next_level = LevelSerializer(read_only=True, source='user.next_level')
    level_ratio = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'phone', 'email', 'points', 'date_joined', 'image', 'birth_date', 'current_level', 'next_level', 'level_ratio', 'daily_target']
    # Get ratio between current level score and next level score 
    def get_level_ratio(self, obj):
        # Check if current level and next level are not None
        current_level = obj.user.current_level
        next_level = obj.user.next_level

        if current_level and next_level:
            current_level_points = current_level.points
            next_level_points = next_level.points

            if current_level_points > 0 and next_level_points > 0:
                ratio = current_level_points / next_level_points
                return math.ceil(ratio * 100)

            # Handle the case where one of the points is zero to avoid division by zero
            if current_level_points == 0 and next_level_points > 0:
                return 0.0  # If current level's points are 0, ratio is 0

        return None  # Handle other cases where either current level or next level is None


    def update(self, instance, validated_data):
        # Update fields in the Customer model
        instance.image = validated_data.get('image', instance.image)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.save()

        # Update fields in the associated User model
        user_data = validated_data.get('user', {})
        user_instance = instance.user

        # Update fields in the User model
        user_instance.email = user_data.get('email', user_instance.email)
        user_instance.phone = user_data.get('phone', user_instance.phone)
        user_instance.first_name = user_data.get('first_name', user_instance.first_name)
        user_instance.country = user_data.get('country', user_instance.country)
        user_instance.save()

        return instance

# Daily Task Serializer 
class DailyTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['user', 'daily_target']

