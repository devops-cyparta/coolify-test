from django.urls import path 
from rest_framework.routers import DefaultRouter 
from .views import PlanViewSet, subscribe_to_plan



router = DefaultRouter()
router.register('plans', PlanViewSet, basename='subscription_plans')


urlpatterns = [
    path('plan/subscribe/', subscribe_to_plan, name='plan_subscribe')
]
urlpatterns += router.urls 
