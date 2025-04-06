from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from core.views import RegisterView
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('customers', views.CustomerViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('get_number_of_users/', views.get_number_of_users, name='get_number_of_users'),
    path('daily_tasks/', views.patch_daily_task, name='patch_daily_task'),
    path('acheivements/', views.patch_achievements, name='patch_achievements'),
]