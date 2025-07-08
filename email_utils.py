import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import datetime

def send_failure_email(image_path, time=None):
    sender_email = ""
    receiver_email = ""
    app_password = ""  # رمز عبور برنامه‌ای Gmail

    if not time:
        time = datetime.datetime.now()

    subject = "🔐 هشدار: ورود ناموفق به سیستم تشخیص چهره"
    body = f"در تاریخ {time.strftime('%Y/%m/%d')} ساعت {time.strftime('%H:%M:%S')} یک ورود ناموفق شناسایی شد.\n\nتصویر پیوست‌شده را بررسی کنید."

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    if os.path.exists(image_path):
        with open(image_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(image_path)}")
            msg.attach(part)
    else:
        print("❌ تصویر یافت نشد، ایمیل بدون پیوست ارسال خواهد شد.")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("✅ ایمیل هشدار ارسال شد.")
    except Exception as e:
        print("❌ خطا در ارسال ایمیل:", e)
