from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db import transaction

from users.models import User
from products.models import Product
from .models import Transaction
from .serializers import TransactionSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def exchange(request):
    user = request.user
    product_id = request.data.get("product_id")

    # 只有會員可以兌換
    if user.role != 'member':
        return Response({"error": "只有會員可以兌換!"}, status=403)

    # 檢查 product
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "找不到此商品!"}, status=404)

    # 檢查點數
    if user.points < product.points_required:
        return Response({"error": "點數不足!"}, status=400)

    # 檢查庫存
    if product.stock <= 0:
        return Response({"error": "已沒庫存!"}, status=400)

    with transaction.atomic():
        # 扣點數
        user.points -= product.points_required
        user.save()

        # 扣庫存
        product.stock -= 1
        product.save()

        # 建立交易紀錄
        tx = Transaction.objects.create(
            user=user,
            product=product,
            points_used=product.points_required
        )

    return Response({
        "message": "Exchange successful",
        "remaining_points": user.points,
        "transaction": TransactionSerializer(tx).data
    })

@api_view(['GET'])
def list_transactions(request):
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def member_transactions(request):
    user = request.user 

    transactions = Transaction.objects.filter(user=user).order_by('-id')

    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)