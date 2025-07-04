from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import os
from dotenv import load_dotenv
load_dotenv()

SMTP_EMAIL = os.getenv("SMTP_EMAIL") or "artisticnailsbyharman@gmail.com"
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") or "bdcz hnel zjyw faww"

def send_order_whatsapp_message(
    customer_name,
    phone_number,
    order_id,
    items,
    payment_qr_link,  # This is a link to the image of the QR code
    recipient_email
):
    total = sum(item['price'] for item in items)

    # HTML block for each item
    html_items = ""
    for item in items:
        html_items += f"""
            <div style="margin-bottom: 20px;">
                <p><b>• {item['shape']} {item['design']} {item['colour']}</b> – ₹{item['price']}</p>
                <img src="{item['image']}" alt="Item Image" width="150" style="border:1px solid #ccc; border-radius:8px;" />
            </div>
        """

    subject = f"🧾 Order Confirmation - {order_id} | Artistic Nails"

    html_body = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>🛍️ Thank you for your order, {customer_name}!</h2>
            <p><strong>🧾 Order ID:</strong> {order_id}</p>
            
            <h3>📦 Items:</h3>
            {html_items}
            
            <p><strong>💰 Total:</strong> ₹{total}</p>
            <p>🕒 Your order will be delivered within 7 working days.</p>
            
            <h3>📲 Payment Instructions:</h3>
            <p>Please scan the QR below to complete your payment:</p>
            <img src="https://res.cloudinary.com/dbp6sexpx/image/upload/v1751100303/Screenshot_2025-06-28_at_2.14.39_PM_spqnxs.png" alt="Payment QR" width="180" style="margin-top:10px; border:1px solid #ccc; border-radius:8px;" />
            
            <p>If you've already paid, you can ignore this message. Otherwise, kindly pay to confirm your order.</p>
            <p>Need help? Just message on this Whatsapp Number 9915024883😊</p>
        </body>
        </html>
    """

    # Build the email
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SMTP_EMAIL
    msg["To"] = recipient_email
    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(SMTP_EMAIL, SMTP_PASSWORD)
            smtp.send_message(msg)
            print("✅ Email sent successfully to", recipient_email)
    except Exception as e:
        print("❌ Failed to send email:", e)