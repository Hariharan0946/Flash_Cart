from django.db import models
import uuid
from django.conf import settings

class Order(models.Model):
    STATUS = [('PLACED','PLACED'),('PACKED','PACKED'),('SHIPPED','SHIPPED'),('DELIVERED','DELIVERED'),('CANCELLED','CANCELLED')]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS, default='PLACED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_id = models.UUIDField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
