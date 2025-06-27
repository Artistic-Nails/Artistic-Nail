from twilio.rest import Client

# Twilio credentials
account_sid = 'AC564c012a36f93023b1002d2f2c6ff4f5'
auth_token = '7b21b2ce07ed1dad1be6033ec54cb462'
client = Client(account_sid, auth_token)

# message_text = """
# 🛍️ Thank you for your order, {{ customer_name }}!  
# Here are your order details:

# 🧾 *Order ID:* {{ order_id }}

# 📦 *Items:*
# {% for item in items %}
# • {{ item.shape }} {{ item.design }} {{ item.colour }} – ₹{{ item.price }}
# {% endfor %}

# 💰 *Total:* ₹{{ total }}

# 🕒 Your order will be delivered within 7 working days.

# 📲 *Please complete your payment using the QR code below:*
# {{ payment_qr_link }}

# If you've already paid, you can ignore this. Otherwise, kindly pay to confirm your order.

# Need help? Just reply here 😊
# """

# # Send WhatsApp message
# message = client.messages.create(
#     from_='whatsapp:+14155238886',  # Twilio sandbox number
#     body=message_text,
#     to='whatsapp:+918448811928'  # Your verified number
# )

# print(f"✅ Message sent! SID: {message.sid}")

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
