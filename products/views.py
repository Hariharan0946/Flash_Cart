from rest_framework import viewsets, permissions
from .models import Product, Inventory
from .serializers import ProductSerializer, InventorySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by("-created_at")
    serializer_class = ProductSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def set_stock(self, request, pk=None):
        product = get_object_or_404(Product, pk=pk)
        qty = int(request.data.get("stock",0))
        inv, _ = Inventory.objects.get_or_create(product=product)
        inv.stock = qty
        inv.save()
        return Response({"status":"ok","stock":inv.stock})
