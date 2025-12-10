from channels.generic.websocket import AsyncJsonWebsocketConsumer

class OrderConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.order_id = self.scope['url_route']['kwargs']['order_id']
        self.group_name = f"order_{self.order_id}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content):
        # expected content: {"lat":..., "lng":...}
        await self.channel_layer.group_send(self.group_name, {"type":"location.update","lat": content.get("lat"), "lng": content.get("lng")})

    async def location_update(self, event):
        await self.send_json({"type":"location","lat": event["lat"], "lng": event["lng"]})

    async def status_update(self, event):
        await self.send_json({"type":"status","status": event.get("status")})
