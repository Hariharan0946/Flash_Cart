from rest_framework import serializers
from .models import Product, Inventory

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id","name","price","description")

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ("product","stock","reserved","updated_at")
