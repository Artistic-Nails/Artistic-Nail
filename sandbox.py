import os
import requests
from dotenv import load_dotenv
load_dotenv()

GUPSHUP_API_KEY = os.getenv("GUPSHUP_API_KEY") or "mwley8mf5jetfxdreoughg5oinlzukbk"
GUPSHUP_APP_NAME = os.getenv("GUPSHUP_APP_NAME") or "ArtisticNails"
GUPSHUP_SANDBOX_SOURCE = "917834811114"  # Gupshup Sandbox sender number

def send_order_whatsapp_message(
    customer_name,
    phone_number,  # Must have joined sandbox (E.g. '91XXXXXXXXXX')
    order_id,
    items,  # List of dicts with keys: shape, colour, design, price
    payment_qr_link  # URL to QR code image or text
):
    total = sum(item['price'] for item in items)

    item_lines = "\n".join(
        f"• {item['shape']} {item['design']} {item['colour']} – ₹{item['price']}"
        for item in items
    )

    message_body = (
        f"🛍️ Thank you for your order, {customer_name}!\n"
        f"🧾 Order ID: {order_id}\n\n"
        f"📦 Items:\n{item_lines}\n"
        f"💰 Total: ₹{total}\n\n"
        f"🕒 Delivery in 7 working days.\n"
        f"📲 Pay using this QR: {payment_qr_link}\n\n"
        f"Reply here for help 😊"
    )

    url = "https://api.gupshup.io/sm/api/v1/msg"
    payload = {
        "channel": "whatsapp",
        "source": GUPSHUP_SANDBOX_SOURCE,
        "destination": phone_number,
        "message": message_body,
        "src.name": GUPSHUP_APP_NAME
    }

    headers = {
        "apikey": GUPSHUP_API_KEY,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code in [200, 202]:
        print("✅ Sandbox message sent:", response.json())
    else:
        raise Exception(f"Gupshup Sandbox API error: {response.status_code} - {response.text}")
    
send_order_whatsapp_message(customer_name="Aryan", items="", order_id="123", payment_qr_link="", phone_number="918448811928")