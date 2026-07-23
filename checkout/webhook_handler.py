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

        print("PAYMENT INTENT SUCCEEDED WEBHOOK STARTED")
        
        payment_intent= event.data.object
        payment_intent_id = payment_intent.id
        try:
            order_id = payment_intent.metadata['order_id']
        except KeyError:
            order_id = None
        
        print("PaymentIntent ID:", payment_intent_id)
        print("Order ID from metadata:", order_id)
        
        if not order_id:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | No order_id found',
                status=400)
    
        order= None

        # Try to find existing order
        for attempt in range (1 ,6):
            try: 
                print(f"Attempt {attempt}: looking for order {order_id}")
                order = Order.objects.get(id=order_id)
                print("Order found:", order)
                break 
            except Order.DoesNotExist:
                print(f"Order not found on attempt {attempt}")
                if attempt < 5 :
                    time.sleep(1)

        if order is None:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | Order not found',status=404)
        
        print("Updating order payment status")

        order.stripe_pid = payment_intent_id
        order.payment_status = 'paid'
        order.save()

        print("Order saved successfully")
        #send_order_confirmation_email
        if not order.confirmation_email_sent:
            send_order_confirmation_email(order)
        
        return HttpResponse ( content=f'Webhook received: {event["type"]} | Order updated',status=200)

    def handle_payment_intent_failed(self,event):
        """ Handle the failed payment """
        return HttpResponse(
            content= f'Webhook received:{event["type"]}', status=200)