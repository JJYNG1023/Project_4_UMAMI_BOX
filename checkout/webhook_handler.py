from django.http import HttpResponse

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
        return HttpResponse(
            content= f'Webhook received:{event["type"]}', status=200
        )
    
    def handle_payment_intent_failed(self,event):
        """ Handle the failed payment """
        return HttpResponse(
            content= f'Webhook received:{event["type"]}', status=200
        )