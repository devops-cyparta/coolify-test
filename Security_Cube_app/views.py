from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from rest_framework import permissions, generics
from rest_framework.response import Response
from .Serializers import *
from .pagination import DefaultPagination, TopGamesPagination, FAQPagination
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login 
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q
# from .permissions import *
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.template.loader import render_to_string
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status


class GamesView(viewsets.ModelViewSet):
    permission_classes = [permissions.AllowAny]
    serializer_class = GamesSrializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]#, OrderingFilter
    pagination_class = DefaultPagination
    search_fields = ['name']
    filterset_fields = ['category']
    http_method_names = ['get']
    ordering_fields = ['released_date']

    def get_queryset(self):
        user_plan = self.request.user.user_subscription.plan if hasattr(self.request.user, 'user_subscription') else None
        if user_plan:
            return Games.objects.filter(premium_plan=user_plan)
        else:
            return Games.objects.all() # Return all games if the user has no subscription 




@api_view(['POST'])
@csrf_exempt
@permission_classes((IsAuthenticated,))#IsAdminUser
def adding_points(request):
    if 'points' in request.data:
        user_id = request.user.id
        points = request.data['points']
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        user.points += points
        user.save()

        data = {"message": f"Points added successfully. User points: {user.points}", "status": status.HTTP_200_OK}

    else:
        data = {"message": "You must provide a user id and points", "status": status.HTTP_400_BAD_REQUEST}

    return Response(data, status=status.HTTP_200_OK)


class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = (permissions.AllowAny,)
    http_method_names = ['get']


class TopGamesView(viewsets.ModelViewSet):
    queryset = Games.objects.all().order_by('-game_points')
    pagination_class = TopGamesPagination
    permission_classes = (permissions.AllowAny,)
    serializer_class = TopGamesSerializers
    http_method_names = ['get']


class FrequentlyAskedQuestionsView(viewsets.ModelViewSet):
    queryset = FrequentlyAskedQuestions.objects.all()
    pagination_class = FAQPagination
    permission_classes  = (permissions.AllowAny,)
    serializer_class = FrequentlyAskedQuestionsSerializers
    http_method_names = ['get']


class RankingBoardView(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-points').exclude(is_superuser=True)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user_customer__country']
    permission_classes = (permissions.AllowAny,)
    serializer_class = RankingBoardSerializer
    http_method_names = ['get']
    

class UserFeedbackAndRateView(viewsets.ModelViewSet):
    queryset = FeedbackandRate.objects
    # permission_classes = (permissions.IsAuthenticated,)
    serializer_class = FeedbackandRateSerializer
    http_method_names = ['post', 'get']
    
    def get_queryset(self,):
        user_rate = self.request.GET.get('user_rate',None)
        if user_rate:
            return self.queryset.filter(user_rate=user_rate)
        return self.queryset.all()

    def get_permissions(self):
        if self.request.method in ['POST']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ContactUsView(viewsets.ModelViewSet):
    serializer_class = ContactUsSerializer
    pagination_class = DefaultPagination
    http_method_names= ['post']
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return ContactUs.objects.filter(user=self.request.user)
    
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)


class GoalView(viewsets.ModelViewSet):
    serializer_class = GoalSerializer
    # pagination_class = DefaultPagination
    http_method_names= ['get', 'post']
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Post Subscribed user 
@api_view(['POST'])
def post_subscribe_user(request):
    serializer = SubscribedUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Subscribed Successfully', 'data' : serializer.data}, status=status.HTTP_201_CREATED)
    else : 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)