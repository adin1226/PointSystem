from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from users.models import User
from products.models import Product
from .models import Transaction
from .serializers import TransactionSerializer


@api_view(['POST'])
def exchange(request):
    user_id = request.data.get("user_id")
    product_id = request.data.get("product_id")

    # 檢查 user
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=404)

    # 只有會員可以兌換
    if user.role != 'member':
        return Response({"error": "Only members can exchange"}, status=403)

    # 檢查 product
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return Response({"error": "Product not found"}, status=404)

    # 檢查點數
    if user.points < product.points_required:
        return Response({"error": "Not enough points"}, status=400)

    # 檢查庫存
    if product.stock <= 0:
        return Response({"error": "Out of stock"}, status=400)

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
        "transaction": TransactionSerializer(tx).data
    })

@api_view(['GET'])
def list_transactions(request):
    transactions = Transaction.objects.all()
    serializer = TransactionSerializer(transactions, many=True)
    return Response(serializer.data)