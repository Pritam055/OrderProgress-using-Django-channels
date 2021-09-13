from os import getcwd
from django.db import models
from django.contrib.auth.models import User 
import string, random
from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
import json 
from asgiref.sync import async_to_sync

from django.db.models.query import InstanceCheckMeta 

# Create your models here.

class Momo(models.Model):
    name = models.CharField(max_length = 20)
    price = models.IntegerField(default = 100)
    image = models.CharField(max_length = 255)

    def __str__(self):
        return self.name 

def generate_order_token(size = 10, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

CHOICES = (
    ("Order Received", "Order Received"),
    ("Baking", "Baking"),
    ("Baked", "Baked"),
    ("Out for delivery", "Out for delivery"),
    ("Customer order received", "Customer order received")
)

class Order(models.Model):
    momo = models.ForeignKey(Momo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_token = models.CharField(max_length = 100, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length = 40, choices=CHOICES, default = "Order Received")
    amount = models.IntegerField(default = 0 )

    def save(self, *args, **kwargs):
        if self.id is None:
            self.order_token = generate_order_token()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return self.order_token

    @staticmethod
    def get_order_details(order_token):
        order = Order.objects.filter(order_token= order_token).first()
        data = {}
        data['amount'] = order.amount
        data['status'] = order.status
        data['order_token'] = order.order_token

        progress_percentage = 20

        if order.status=='Order Received':
            progress_percentage = 20 
        elif order.status=='Baking':
            progress_percentage = 40
        elif order.status=='Baked':
            progress_percentage = 60
        elif order.status=='Out for delivery':
            progress_percentage = 80
        elif order.status=='Customer order received':
            progress_percentage = 100 
        data['progress_percentage'] = progress_percentage
        return data

@receiver(post_save, sender=Order)
def order_status_handler(sender, instance, created, **kwargs):
    if not created:

        data = {}
        data['amount'] = instance.amount
        data['status'] = instance.status
        data['order_token'] = instance.order_token

        progress_percentage = 20

        if instance.status=='Order Received':
            progress_percentage = 20 
        elif instance.status=='Baking':
            progress_percentage = 40
        elif instance.status=='Baked':
            progress_percentage = 60
        elif instance.status=='Out for delivery':
            progress_percentage = 80
        elif instance.status=='Customer order received':
            progress_percentage = 100 
        data['progress_percentage'] = progress_percentage
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "order_%s" % instance.order_token,
            {
                'type':'order_status',
                'value': json.dumps(data)
            }
        )