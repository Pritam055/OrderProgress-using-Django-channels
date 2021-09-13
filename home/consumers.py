from channels.generic.websocket import WebsocketConsumer
import json 
from asgiref.sync import async_to_sync

from .models import Order

class OrderProgressConsumer(WebsocketConsumer):
    
    def connect(self):
        self.order_token = self.scope['url_route']['kwargs']['order_token']
        self.room_group_name = "order_%s" % self.order_token
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        order = Order.get_order_details(self.order_token)
        self.send(text_data = json.dumps({
            "payload": order
        }))

    def receive(self, data):
        print(data)
        """ async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type': 'order_status',
                'payload': data
            }
        ) """

    def order_status(self, event):
        data = json.loads(event['value'])
        print(data, type(data))
        self.send(text_data = json.dumps({'payload': data}))

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )