from rest_framework import serializers
from .models import *
from django.contrib.auth import login,authenticate
from django_countries.serializer_fields import CountryField
from core.serializers import UserSerializer


class SimilarGamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['id', 'pic', 'game_points', 'name', 'description']


class GamesFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['id', 'name']

             
class GamesSrializer(serializers.ModelSerializer):
    feedbacks=serializers.SerializerMethodField('get_feedbacks')
    similar_games = serializers.SerializerMethodField('get_similar_games')
    class Meta:
        model = Games
        fields = '__all__'
        # depth = 1

    def get_feedbacks(self, obj):
        feedbacks = obj.feedbacks.values()
        return feedbacks

    def get_similar_games(self, obj):
        similar_games = Games.objects.filter(category__in=obj.category.all()).exclude(id=obj.id).distinct()[:3]
        return SimilarGamesSerializer(similar_games, many=True).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

   
class TopGamesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = '__all__'
        depth = 1


class FrequentlyAskedQuestionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = FrequentlyAskedQuestions
        fields = '__all__'


class RankingBoardSerializer(serializers.ModelSerializer):
    flag = serializers.URLField(source='user_customer.country.flag')
    country = CountryField(source='user_customer.country')
    
    class Meta:
        model = User
        fields = ('first_name','points','flag','country')        


# class GameSerializers(serializers.ModelSerializer):
 
#     class Meta:
#         model = Games
#         fields = '__all__'
#         depth = 1


class ContactUsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUs
        fields = ['id', 'first_name', 'last_name', 'phone', 'message']
        extra_kwargs = {
            'user': {'read_only': True},
        }


class GoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Goal
        fields = ['id', 'user', 'set_time', 'start_time', 'end_time']
        extra_kwargs = {
            'user': {'read_only': True},
        }


class FeedbackandRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackandRate
        fields = '__all__'
        extra_kwargs = {
            'user': {'read_only': True},
            'date': {'read_only': True},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user = instance.user
        games = instance.games
        representation['user'] = UserSerializer(user).data
        representation['games'] = GamesFeedbackSerializer(games).data
        return representation
    

class SubscribedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscribedUser 
        fields = '__all__' 