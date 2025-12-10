from django.db import transaction
from .models import Inventory
from django.core.exceptions import ObjectDoesNotExist

class OutOfStock(Exception):
    pass

def reserve_stock(product_id, qty):
    with transaction.atomic():
        inv = Inventory.objects.select_for_update().get(product_id=product_id)
        if inv.stock < qty:
            raise OutOfStock("Not enough stock")
        inv.stock -= qty
        inv.reserved += qty
        inv.save()
