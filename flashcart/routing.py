from django.urls import re_path
from tracking.consumers import OrderTrackingConsumer

websocket_urlpatterns = [
    re_path(r"ws/track/(?P<order_id>\d+)/$", OrderTrackingConsumer.as_asgi()),
]
