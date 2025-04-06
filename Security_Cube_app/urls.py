
from django.urls import path, include
from Security_Cube_app import views
from rest_framework import routers
from .views import *

r = routers.DefaultRouter()
r.register('game', views.GamesView, basename='games')
r.register('category', views.CategoryView, basename='categories')
r.register('topgames', views.TopGamesView, basename='top-games')
r.register('question', views.FrequentlyAskedQuestionsView, basename='questions')
r.register('ranking',views.RankingBoardView, basename='rankings')
r.register('feedback',views.UserFeedbackAndRateView, basename='feedbacks')
r.register('contactus',views.ContactUsView, basename='contactus')
r.register('goal',views.GoalView, basename='goal')


urlpatterns = [
    path('api/', include(r.urls)),
    path("points/", views.adding_points, name="adding-points"),
    path('subscribe/', views.post_subscribe_user, name='post_subscribe_user'),
]
