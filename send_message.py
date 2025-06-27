from twilio.rest import Client
import os
# Twilio credentials
account_sid = os.getenv("ACC_SID")
auth_token = os.getenv("AUTH_TOKEN")
client = Client(account_sid, auth_token)

def send_order_whatsapp_message(
    customer_name,
    phone_number,  # E.g. '+91XXXXXXXXXX'
    order_id,
    items,  # List of dicts with keys: shape, colour, design, price
    payment_qr_link,  # URL to QR code image or text
    twilio_whatsapp_number='whatsapp:+14155238886'  # Default Twilio sandbox number
):
    client = Client(account_sid, auth_token)

    total = sum(item['price'] for item in items)

    # Create the message body
    item_lines = ""
    for item in items:
        item_lines += f"• {item['shape']} {item['design']} {item['colour']} – ₹{item['price']}\n"

    message_body = (
        f"🛍️ Thank you for your order, {customer_name}!\n"
        f"🧾 *Order ID:* {order_id}\n\n"
        f"📦 *Items:*\n{item_lines}\n"
        f"💰 *Total:* ₹{total}\n\n"
        f"🕒 Your order will be delivered within 7 working days.\n\n"
        f"📲 *Please complete your payment using the QR below:*\n{payment_qr_link}\n\n"
        f"If you've already paid, you can ignore this. Otherwise, kindly pay to confirm your order.\n\n"
        f"Need help? Just reply here 😊"
    )

    # Send the WhatsApp message
    message = client.messages.create(
        from_=twilio_whatsapp_number,
        to=f'whatsapp:{phone_number}',
        body=message_body
    )

    return message.sid
