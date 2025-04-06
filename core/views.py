from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.decorators import action
from .serializers import UserCreateSerializer, CustomerSerializer, UserSerializer, DailyTaskSerializer
from .models import Customer, User
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET', 'PUT', 'PATCH'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = get_object_or_404(Customer, user_id=request.user.id)

        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)

        elif request.method in ['PUT', 'PATCH']:
            customer_serializer = CustomerSerializer(customer, data=request.data, partial=True)
            user_serializer = UserSerializer(customer.user, data=request.data, partial=True)

            customer_serializer.is_valid(raise_exception=True)
            user_serializer.is_valid(raise_exception=True)

            customer_serializer.save()
            user_serializer.save()

            return Response(customer_serializer.data)
        

@api_view(['GET'])
def get_number_of_users(request):
    try:
        # Use the Django User model to get the count of users
        number_of_users = User.objects.count()

        # Return the result as a DRF Response
        return Response({'number_of_users': number_of_users})
    except Exception as e:
        # Handle exceptions if any
        return Response({'error': str(e)}, status=500)
 

 # Patch Daily Task 
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def patch_daily_task(request):
    user = request.user 
    daily_target = request.GET.get('daily_target', None)

    if daily_target is None:
        return Response({"message": "daily_target parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user.daily_target = daily_target 
        user.save()

        return Response({"message": "Daily target updated successfully", "daily_target": user.daily_target}, status=status.HTTP_200_OK)

    except ValueError as ve:
        return Response({"message": f"Invalid daily_target value: {daily_target}. {str(ve)}"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(['PATCH'])
def patch_achievements(request):
    user = request.user 
    achieved_daily_target = request.GET.get('achieved_daily_target')
    if achieved_daily_target is None :
        return Response({'message' : 'Achieved Daily Target Parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user.achieved_daily_target = achieved_daily_target 
        user.save()

        return Response({"message": "achieved_daily_target updated successfully", "achieved_daily_target": user.achieved_daily_target}, status=status.HTTP_200_OK)

    except ValueError as ve:
        return Response({"message": f"Invalid achieved_daily_target value: {achieved_daily_target}. {str(ve)}"}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

