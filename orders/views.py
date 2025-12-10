from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db import transaction
from .models import Order, OrderItem
from products.services import reserve_stock, OutOfStock
from .tasks import send_order_confirmation, schedule_auto_cancel

class PlaceOrderView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        items = request.data.get("items", [])
        if not items:
            return Response({"detail":"no items"}, status=status.HTTP_400_BAD_REQUEST)
        total = 0
        try:
            with transaction.atomic():
                for it in items:
                    pid = it.get("product_id")
                    qty = int(it.get("quantity",1))
                    price = float(it.get("price",0))
                    reserve_stock(pid, qty)
                    total += price * qty
                order = Order.objects.create(user=request.user, total_amount=total)
                for it in items:
                    OrderItem.objects.create(order=order, product_id=it.get("product_id"), quantity=it.get("quantity"), price=it.get("price"))
        except OutOfStock as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        # trigger tasks via Celery
        send_order_confirmation.delay(str(order.id))
        schedule_auto_cancel.apply_async(args=[str(order.id)], countdown=15*60)
        return Response({"order_id": str(order.id)}, status=status.HTTP_201_CREATED)
