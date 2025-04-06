from django.utils import timezone
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated 
from rest_framework import status 
from rest_framework.response import Response
from .serializers import PlanSerializer 
from .models import Plan 
from .serializers import PlanSerializer
from .models import Games, Plan, Subscription


# Plan VuewSet 
class PlanViewSet(ModelViewSet):
    http_method_names = ('get')
    serializer_class = PlanSerializer 
    queryset = Plan.objects.all()
    permission_classes = [AllowAny]

# Subscribe to plan 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def subscribe_to_plan(request):
    plan_id = request.POST.get('plan_id')
    if 'plan_id' not in request.data : 
        return Response({'message' : 'plan_id is required in query paramters '})
    try:
        selected_plan = Plan.objects.get(pk=plan_id)
    # if plan doesn't exist 
    except Plan.DoesNotExist:
        return Response({'message': 'Plan not found'}, status=status.HTTP_404_NOT_FOUND)
    # Existing Subscription 
    existing_subscription = Subscription.objects.filter(user=request.user, plan=selected_plan, expiring_date__gt=timezone.now()).first()
    if existing_subscription:
        return Response({'message': 'User already has an active subscription for this plan'}, status=status.HTTP_400_BAD_REQUEST)
    expiring_date = timezone.now() + timezone.timedelta(days=356)  # @expiring date after 356 days 
    new_subscription = Subscription.objects.create(user=request.user, plan=selected_plan, expiring_date=expiring_date)
    return Response({'message' : 'User Subscribed Successfully'}, status=status.HTTP_201_CREATED)


