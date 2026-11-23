import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Điền Gmail và Mật khẩu ứng dụng (App Password 16 ký tự) của bạn vào đây để gửi thật
SENDER_EMAIL = "email_cua_ban@gmail.com"
SENDER_PASSWORD = "xxxx xxxx xxxx xxxx"

def send_order_status_email(receiver_email, order_id, customer_name, new_status):
    status_map = {
        'pending': 'Chờ xác nhận',
        'shipping': 'Đang giao hàng',
        'completed': 'Hoàn thành',
        'cancelled': 'Đã hủy',
    }
    status_vn = status_map.get(new_status, new_status)

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg["Subject"] = f"[ElectroStore] Cập nhật trạng thái đơn hàng #{order_id}"

    body = (
        f"Xin chào {customer_name},\n\n"
        f"Đơn hàng #{order_id} của bạn đã được cập nhật trạng thái sang: {status_vn}.\n"
        f"Cảm ơn bạn đã mua sắm tại cửa hàng!\n"
    )
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        # Kết nối SMTP SSL cổng 465 giống slide Chapter 6
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=10) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        return True, f"Đã gửi email thông báo tới {receiver_email}"
    except Exception as e:
        return False, f"Đã lưu trạng thái (Chưa gửi được email: {e})"