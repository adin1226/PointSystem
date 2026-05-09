from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from rest_framework import generics
from .models import User
from .serializers import RegisterSerializer
from .serializers import UserSerializer
from .serializers import CustomTokenSerializer
from django.shortcuts import render
from products.models import Product

class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def login_page(request):
    return render(request, "login.html")

def register_page(request):
    return render(request, "register.html")

# @api_view(['POST'])
# def create_user(request):
#     serializer = UserSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     return Response(serializer.errors, status=400)


@api_view(['GET'])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_user(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_now_user(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def add_points(request):
    # try:
    #     user = User.objects.get(id=pk)
    # except User.DoesNotExist:
    #     return Response({"error": "User not found"}, status=404)
    user = request.user

    # 儲值只有會員限定
    if user.role != 'member':
        return Response({"error": "Only members can deposit"}, status=403)

    amount = int(request.data.get("amount", 0))

    if amount <= 0:
        return Response({"error": "Invalid amount"}, status=400)

    user.points += int(amount)
    user.save()

    return Response({
        "message": "Points added",
        "points": user.points
    })