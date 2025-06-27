import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()

SMTP_EMAIL = os.getenv("SMTP_EMAIL") or "artisticnailsbyharman@gmail.com"
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") or "bdcz hnel zjyw faww"

def send_order_whatsapp_message(  # renamed but reused for email
    customer_name,
    phone_number,  # Can ignore or use in body
    order_id,
    items,
    payment_qr_link,
    recipient_email  # where to send email
):
    total = sum(item['price'] for item in items)

    item_lines = "\n".join(
        f"• {item['shape']} {item['design']} {item['colour']} – ₹{item['price']}"
        for item in items
    )

    subject = f"🧾 Order Confirmation - {order_id} | Artistic Nails"
    body = (
        f"🛍️ Thank you for your order, {customer_name}!\n"
        f"🧾 Order ID: {order_id}\n\n"
        f"📦 Items:\n{item_lines}\n"
        f"💰 Total: ₹{total}\n\n"
        f"🕒 Your order will be delivered within 7 working days.\n"
        f"📲 Please complete your payment using the QR below:\n{payment_qr_link}\n\n"
        f"If you've already paid, you can ignore this. Otherwise, kindly pay to confirm your order.\n\n"
        f"Need help? Just reply to this email 😊"
    )

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SMTP_EMAIL
    msg['To'] = recipient_email
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
            smtp.send_message(msg)
            print("✅ Email sent successfully to", recipient_email)
    except Exception as e:
        print("❌ Failed to send email:", e)

send_order_whatsapp_message(
    customer_name="Aryan",
    phone_number="8448811928",
    order_id="123",
    items=[{"shape": "Round", "design": "Floral", "colour": "Red", "price": 399}],
    payment_qr_link="https://example.com/qr",
    recipient_email="aryanmanchanda@hotmail.com"
)