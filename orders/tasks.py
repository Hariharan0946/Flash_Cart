# task. When running with Celery, these will be executed by workers.

from celery import shared_task
from .models import Order
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@shared_task
def send_order_confirmation(order_id):
    # Placeholder: send email or sms in real app
    print(f"[TASK] send_order_confirmation for order {order_id}")
    # notify via channels group
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f"order_{order_id}", {"type":"status.update","status":"PLACED"})
    except Exception as e:
        print("Channels notify failed:", e)

@shared_task
def schedule_auto_cancel(order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.status == "PLACED":
            order.status = "CANCELLED"
            order.save()
            print(f"[TASK] Auto-cancelled order {order_id}")
    except Order.DoesNotExist:
        pass
