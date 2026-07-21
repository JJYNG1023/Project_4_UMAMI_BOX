from django.conf import settings
from django.core.mail import send_mail

"""Send order confirmation email to the customer."""
def send_order_confirmation_email(order):

    if order.confirmation_email_sent:
        return

    order_reference = f"UMAMI-{order.id:05d}"

    order_items = ""

    for item in order.lineitems.all():
        order_items += (
            f"- {item.product.name} x {item.quantity} "
            f"= £{item.lineitem_total}\n"
        )

    subject = f"Your Umami Box order confirmation - {order_reference}"

    message = f"""
        Hi {order.full_name},

        Thank you for your order.

        Your order has been placed successfully.

        Order Reference: {order_reference}
        Payment Status: {order.payment_status.title()}
        Total Paid: £{order.grand_total}

        Delivery Date: {order.delivery_date}
        Delivery Time: {order.delivery_time}

        Order Items:
        {order_items}

        Delivery Address:
        {order.street_address_1}
        {order.street_address_2}
        {order.town_or_city}
        {order.postcode}
        {order.country}

        Thank you for ordering from Umami Box.

        Kind regards,
        Umami Box
        """

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.email],
        fail_silently=False,
    )

    order.confirmation_email_sent = True
    order.save(update_fields=['confirmation_email_sent'])