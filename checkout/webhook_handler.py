from django.http import HttpResponse

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
                content= f'Webhook received: payment_intent.succeeded | No order_id found', status=200
            )

        try:
            order = Order.objects.get(id=order_id)

            order.stripe_pid = payment_intent_id
            order.payment_status = 'paid'
            order.save()

            send_order_confirmation_email(order)

            return HttpResponse(
                content=f'Webhook received: {event["type"]} | Order updated',
                status=200
            )

        except Order.DoesNotExist:
            return HttpResponse(
                content=f'Webhook received: {event["type"]} | Order not found',
                status=404
            )

    def handle_payment_intent_failed(self,event):
        """ Handle the failed payment """
        return HttpResponse(
            content= f'Webhook received:{event["type"]}', status=200
        )