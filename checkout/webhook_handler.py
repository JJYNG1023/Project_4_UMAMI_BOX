from django.http import HttpResponse
import time

from .models import Order
from .utils import send_order_confirmation_email

class StripeWH_Handler:
    """ Handle stripe webhook"""
    def __init__(self,request):
        self.request = request

    def handle_event(self,event):
        """ Handle a generic/unknown webhook event """
        return HttpResponse(
            content= f'Webhook received:{event["type"]}', status=200
        )
    
    def handle_payment_intent_succeeded(self,event):
        """ Handle the success payment """
        payment_intent= event.data.object
        payment_intent_id = payment_intent.id
        order_id = payment_intent.metadata.get('order_id')
        
        if not order_id:
            return HttpResponse(
                content=f'webhook recieved: {event['type']} | success: verified order already in database', status = 200
            )
    
        order= None

        # Try to find existing order
        for attempt in range (1 ,6):
            try: 
                order = Order.objects.get(id=order_id)
                break 
            except Order.DoesNotExist:
                if attempt < 5 :
                time.sleep(1)

        if order is None:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | Order not found',status=404)
        
        order.stripe_pid = payment_intent_id
        order.payment_status = 'paid'
        order.save()

        send_order_confirmation_email(order)
        return HttpResponse ( content=f'Webhook received: {event["type"]} | Order updated',status=200)

    def handle_payment_intent_failed(self,event):
        """ Handle the failed payment """
        return HttpResponse(
            content= f'Webhook received:{event["type"]}', status=200)