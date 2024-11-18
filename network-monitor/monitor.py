import ping3
import smtplib
from email.mime.text import MIMEText
import time
from datetime import datetime
from config import *

def check_host(ip):
    """Ping host and return response time or None if unreachable"""
    try:
        response_time = ping3.ping(ip)
        return response_time
    except Exception:
        return None

def send_alert(ip, status, response_time=None):
    """Send email alert for host status change"""
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(SMTP_EMAIL, SMTP_PASSWORD)
            
            for recipient in ALERT_EMAILS:
                # Create a new message for each recipient
                body = f"""
                Host: {ip}
                Status: {status}
                Time: {datetime.now()}
                Response Time: {response_time if response_time else 'N/A'} ms
                """
                
                msg = MIMEText(body)
                msg['Subject'] = f"Network Alert - {ip} is {status}"
                msg['From'] = SMTP_EMAIL
                msg['To'] = recipient
                server.send_message(msg)
                
    except Exception as e:
        print(f"Failed to send email: {e}")

def monitor_network():
    """Main monitoring loop"""
    host_status = {ip: True for ip in TARGET_IPS}  # True = up, False = down
    
    while True:
        for ip in TARGET_IPS:
            response_time = check_host(ip)
            current_status = response_time is not None
            
            if current_status != host_status[ip]:
                status_str = "UP" if current_status else "DOWN"
                send_alert(ip, status_str, response_time)
                host_status[ip] = current_status
            
            print(f"{datetime.now()} - {ip}: {'UP' if current_status else 'DOWN'} - {response_time}ms")
        
        time.sleep(CHECK_INTERVAL)
